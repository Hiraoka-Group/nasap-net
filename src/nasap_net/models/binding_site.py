from dataclasses import dataclass

from nasap_net.types import ID, SupportsDunderLt


@dataclass(frozen=True, order=True)
class BindingSite(SupportsDunderLt):
    """A specific binding site on a specific component."""
    component_id: ID
    site_id: ID
