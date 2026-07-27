"""Query objects for infrastructure-backed reads."""

from kp_compiler.infrastructure.queries.outcome_queries import (
    ExistingObjectTitlesQuery,
    ExplicitAliasLookupQuery,
    ObjectCountQuery,
    OrphanAliasQuery,
    TagCoverageQuery,
    TopAliasLookupQuery,
)
from kp_compiler.infrastructure.queries.pack_queries import DependencyDomainQuery, DependencyObjectIdentifiersQuery

__all__ = [
    "DependencyDomainQuery",
    "DependencyObjectIdentifiersQuery",
    "ExistingObjectTitlesQuery",
    "ExplicitAliasLookupQuery",
    "ObjectCountQuery",
    "OrphanAliasQuery",
    "TagCoverageQuery",
    "TopAliasLookupQuery",
]
