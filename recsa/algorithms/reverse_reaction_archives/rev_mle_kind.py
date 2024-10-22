from recsa import MleKind

__all__ = ['get_rev_mle_kind']


def get_rev_mle_kind(reaction_kind: MleKind) -> MleKind:
    return MleKind(
        metal=reaction_kind.metal,
        leaving=reaction_kind.entering,
        entering=reaction_kind.leaving)
