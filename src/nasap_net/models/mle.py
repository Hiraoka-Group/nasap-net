from dataclasses import dataclass

from nasap_net.exceptions import NasapNetError
from nasap_net.models import BindingSite


@dataclass(frozen=True)
class MLEKind:
    metal: str
    leaving: str
    entering: str


class DuplicationNotSetError(NasapNetError):
    pass


@dataclass(frozen=True, init=False)
class MLE:
    metal: BindingSite
    leaving: BindingSite
    entering: BindingSite
    _duplication: int | None = None

    def __init__(
            self,
            metal: BindingSite,
            leaving: BindingSite,
            entering: BindingSite,
            *,
            duplication: int | None = None
    ) -> None:
        object.__setattr__(self, 'metal', metal)
        object.__setattr__(self, 'leaving', leaving)
        object.__setattr__(self, 'entering', entering)
        object.__setattr__(self, '_duplication', duplication)

    @property
    def duplication(self) -> int:
        if self._duplication is None:
            raise DuplicationNotSetError("Duplication count is not set.")
        return self._duplication
