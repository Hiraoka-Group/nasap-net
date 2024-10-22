from dataclasses import dataclass

__all__ = ['MleKind']

# QUESTION: Should I use pydantic's dataclass instead of dataclass?
@dataclass(frozen=True, eq=True)
class MleKind:
    metal: str
    leaving: str
    entering: str

    def __hash__(self):
        return hash((self.metal, self.leaving, self.entering))
