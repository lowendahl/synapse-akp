"""Query objects used by compiler stages."""

from kp_compiler.stages.project.queries.outcome_queries import (
    ExistingObjectTitlesQuery,
    ExplicitAliasLookupQuery,
    ObjectCountQuery,
    OrphanAliasQuery,
    TagCoverageQuery,
    TopAliasLookupQuery,
)
from kp_compiler.stages.project.queries.pack_queries import DependencyDomainQuery, DependencyObjectIdentifiersQuery

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
