from dataclasses import dataclass
from typing import Generic, Mapping

from nasap_net import Assembly
from reverse_reaction_pairing.core import Reaction, _A


@dataclass(frozen=True)
class RichReactionView(Generic[_A]):
    reaction: Reaction
    assemblies: Mapping[_A, Assembly]

    @property
    def init_assembly(self) -> Assembly:
        return self.assemblies[self.reaction.init_assem_id]

    @property
    def entering_assembly(self) -> Assembly | None:
        if self.reaction.entering_assem_id is None:
            return None
        return self.assemblies[self.reaction.entering_assem_id]

    @property
    def product_assembly(self) -> Assembly:
        return self.assemblies[self.reaction.product_assem_id]

    @property
    def leaving_assembly(self) -> Assembly | None:
        if self.reaction.leaving_assem_id is None:
            return None
        return self.assemblies[self.reaction.leaving_assem_id]
