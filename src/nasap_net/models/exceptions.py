from dataclasses import dataclass

from .assembly import Assembly


@dataclass
class InconsistentComponentBetweenAssembliesError(Exception):
    """Raised when there are inconsistent definitions for a component kind
    between different assemblies.
    """
    component_kind: str
    assembly1: Assembly
    assembly2: Assembly

    def __str__(self) -> str:
        return (
            f'Inconsistent definitions for component kind '
            f'"{self.component_kind}" between assemblies: '
            f'Assembly 1: {self.assembly1}, Assembly 2: {self.assembly2}.'
        )
