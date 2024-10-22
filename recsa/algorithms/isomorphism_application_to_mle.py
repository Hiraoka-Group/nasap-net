from collections.abc import Mapping

from recsa import MleBindsite

__all__ = ['apply_isomorphism_to_mle']


def apply_isomorphism_to_mle(
        mle_bindsite: MleBindsite, isomorphism: Mapping[str, str]
        ) -> MleBindsite:
    return MleBindsite(
        metal=isomorphism[mle_bindsite.metal],
        leaving=isomorphism[mle_bindsite.leaving],
        entering=isomorphism[mle_bindsite.entering]
    )
