from dataclasses import dataclass


@dataclass(frozen=True)
class _MLE:
    metal: str
    leaving: str
    entering: str
