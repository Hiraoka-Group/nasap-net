class InconsistentComponentKindError(Exception):
    """Raised when there are inconsistent definitions for a component kind,
    i.e., the same kind name corresponds to different component structures.
    """
    def __init__(
            self,
            component_kind: str,
            message: str = (
                    'Components with the same kind must have the same '
                    'structure, including site IDs'
            )
    ) -> None:
        self.component_kind = component_kind
        super().__init__(f'{message}: Kind: "{component_kind}".')
