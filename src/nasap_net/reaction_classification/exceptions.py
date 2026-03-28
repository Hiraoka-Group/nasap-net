from nasap_net import Reaction


class IncompleteReactionClassifierError(Exception):
    """
    Raised by user-defined classification functions when a reaction
    cannot be classified due to incomplete rules.

    Users should raise this exception at branches that are expected
    to be unreachable.

    Parameters
    ----------
    reaction : Reaction
        The reaction that could not be classified.

    error_id : str, optional
        Identifier to distinguish multiple raise points within the same
        classification function.

    Examples
    --------
    >>> def classify_reaction(reaction):
    ...     if reaction.leaving_kind == 'X':
    ...         if reaction.entering_kind == 'L':
    ...             return '1f'
    ...         else:
    ...             raise IncompleteReactionClassifierError(
    ...                 reaction, error_id="case_X_other"
    ...             )
    ...     else:
    ...         raise IncompleteReactionClassifierError(
    ...             reaction, error_id="case_not_X"
    ...         )
    """

    def __init__(self, reaction: Reaction, error_id: str | None = None):
        self.reaction = reaction
        self.error_id = error_id

        message = "Incomplete reaction classification rule"
        if error_id is not None:
            message += f" (error_id={error_id})"

        super().__init__(message)

    def __str__(self):
        base = super().__str__()
        return f"{base} | reaction: {self.reaction}"
