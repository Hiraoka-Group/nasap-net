import logging
from collections.abc import Callable, Iterable

from nasap_net import Reaction

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

def classify_reactions(
        reactions: Iterable[Reaction],
        classifier: Callable[[Reaction], str],
) -> dict[Reaction, str]:
    result = {}
    for reaction in reactions:
        cls = classifier(reaction)
        result[reaction] = cls

        logger.info("%s -> %s", reaction, cls)

    return result
