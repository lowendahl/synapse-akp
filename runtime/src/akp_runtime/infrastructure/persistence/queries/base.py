"""Base query protocol and executor for DuckDB pack queries.

What: Abstract base for all pack query objects.
Why: Uniform execution pattern, testable in isolation, SQL confined to query files.
Boundaries: Only files in queries/ directory may contain SQL strings.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

import duckdb

from akp_runtime.contracts.errors import PackQueryError, RuntimeStateError
from akp_runtime.contracts.protocols import QueryExecutorProtocol

ResultT = TypeVar("ResultT")


class PackQuery(ABC, Generic[ResultT]):
    """Abstract base for all knowledge pack queries.

    Subclasses define the SQL and parameters; the executor handles
    connection lifecycle and error translation.
    Implements QueryObjectProtocol from contracts.
    """

    @abstractmethod
    def sql(self) -> str:
        """Return the SQL statement to execute."""

    @abstractmethod
    def parameters(self) -> list[Any]:
        """Return the bound parameters for the query."""

    @abstractmethod
    def map_results(self, rows: list[tuple]) -> ResultT:
        """Transform raw row tuples into domain objects."""

    @property
    def context_name(self) -> str:
        """Human-readable name for error messages."""
        return self.__class__.__name__


class QueryExecutor(QueryExecutorProtocol):
    """Executes PackQuery objects against a DuckDB connection.

    Translates DuckDB errors into domain-specific exceptions.
    Implements QueryExecutorProtocol from contracts.
    """

    def __init__(self, connection: duckdb.DuckDBPyConnection, pack_id: str) -> None:
        self._connection = connection
        self._pack_id = pack_id
        self._closed = False

    def mark_closed(self) -> None:
        """Mark the executor as closed (connection no longer usable)."""
        self._closed = True

    def execute(self, query: PackQuery[ResultT]) -> ResultT:
        """Execute a query and return mapped results."""
        if self._closed:
            raise RuntimeStateError(
                operation=query.context_name,
                reason="Pack connection is closed",
            )
        try:
            params = query.parameters()
            result = self._connection.execute(query.sql(), params) if params else self._connection.execute(query.sql())
            rows = result.fetchall()
            return query.map_results(rows)
        except (RuntimeStateError, PackQueryError):
            raise
        except Exception as error:
            raise PackQueryError(
                pack_id=self._pack_id,
                query_context=query.context_name,
                detail=str(error),
            ) from error
