from dataclasses import dataclass

__all__ = ['MleBindsite']


@dataclass(frozen=True, eq=True, order=True)
class MleBindsite:
    metal: str
    leaving: str
    entering: str

    def __hash__(self):
        return hash((self.metal, self.leaving, self.entering))
