import itertools
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Iterable, Iterator

from nasap_net.models import Assembly, BindingSite
from nasap_net.reaction_exploration_im.lib import \
    extract_unique_site_combinations
from nasap_net.reaction_exploration_im.lib.separation import \
    separate_if_possible
from nasap_net.reaction_exploration_im.models import MLE, MLEKind, \
    Reaction


class ReactionExplorer(ABC):
    def explore(self) -> Iterator[Reaction]:
        mles = self._iter_mles()
        unique_mles = self._get_unique_mles(mles)
        for mle in unique_mles:
            yield self._perform_reaction(mle)

    @abstractmethod
    def _iter_mles(self) -> Iterator[MLE]:
        pass

    @abstractmethod
    def _get_unique_mles(self, mles: Iterable[MLE],) -> Iterator[MLE]:
        pass

    @abstractmethod
    def _perform_reaction(self, mle: MLE) -> Reaction:
        pass


@dataclass(frozen=True)
class IntraReactionExplorer(ReactionExplorer):
    assembly: Assembly
    mle_kind: MLEKind

    def _iter_mles(self) -> Iterator[MLE]:
        """Get all possible MLEs for intra-molecular reactions in an assembly.

        This function generates all MLEs (combinations of metal binding sites,
        leaving binding sites, and entering binding sites) for intra-molecular
        reactions within a given assembly based on the specified component kinds.

        Returned MLEs meet the following conditions:
          - The metal binding site and leaving binding site are connected to each
            other.
          - The component kind of the metal binding site is `mle_kind.metal`.
          - The component kind of the leaving binding site is `mle_kind.leaving`.
          - The entering binding site is free and has the component kind
            `mle_kind.entering`.
        """
        # Pairs of metal binding sites and leaving binding sites
        # that meet the following conditions:
        # - The binding sites are connected to each other
        # - The component kind of the metal binding site is mle_kind.metal
        # - The component kind of the leaving binding site is mle_kind.leaving
        ml_pair: list[tuple[BindingSite, BindingSite]] = []
        for bond in self.assembly.bonds:
            site1, site2 = bond.sites
            kind1 = self.assembly.get_component_kind_of_site(site1)
            kind2 = self.assembly.get_component_kind_of_site(site2)
            match (kind1, kind2):
                case (self.mle_kind.metal, self.mle_kind.leaving):
                    ml_pair.append((site1, site2))
                case (self.mle_kind.leaving, self.mle_kind.metal):
                    ml_pair.append((site2, site1))

        # Entering binding sites that meet the following conditions:
        # - The binding site is free
        # - The component kind of the entering binding site is mle_kind.entering
        entering_sites = self.assembly.find_sites(
            has_bond=False, component_kind=self.mle_kind.entering)

        for (metal, leaving), entering in itertools.product(
                ml_pair, entering_sites):
            yield MLE(metal, leaving, entering)

    def _get_unique_mles(self, mles: Iterable[MLE]) -> Iterator[MLE]:
        unique_mle_trios = extract_unique_site_combinations(
            [(mle.metal, mle.leaving, mle.entering) for mle in mles],
             self.assembly)
        for unique_mle in unique_mle_trios:
            metal, leaving, entering = unique_mle.site_comb
            yield MLE(
                metal, leaving, entering,
                duplication=unique_mle.duplication)

    def _perform_reaction(self, mle: MLE) -> Reaction:
        raw_product = (
            self.assembly
                .remove_bond(mle.metal, mle.leaving)
                .add_bond(mle.metal, mle.entering)
        )

        product, leaving = separate_if_possible(
            raw_product, mle.metal.component_id)

        return Reaction(
            init_assem=self.assembly,
            entering_assem=None,
            product_assem=product,
            leaving_assem=leaving,
            metal_bs=mle.metal,
            leaving_bs=mle.leaving,
            entering_bs=mle.entering,
            duplicate_count=mle.duplication
        )


@dataclass(frozen=True)
class InterReactionExplorer(ReactionExplorer):
    init_assembly: Assembly
    entering_assembly: Assembly
    mle_kind: MLEKind

    def _iter_mles(self) -> Iterator[MLE]:
        raise NotImplementedError()

    def _get_unique_mles(self, mles: Iterable[MLE]) -> Iterator[MLE]:
        unique_ml_pairs = extract_unique_site_combinations(
            [(mle.metal, mle.leaving) for mle in mles], self.init_assembly)
        unique_entering_sites = extract_unique_site_combinations(
            [(mle.entering,) for mle in mles], self.entering_assembly)
        for unique_ml, unique_e in itertools.product(
                unique_ml_pairs, unique_entering_sites):
            metal, leaving = unique_ml.site_comb
            (entering,) = unique_e.site_comb
            yield MLE(
                metal, leaving, entering,
                duplication=unique_ml.duplication * unique_e.duplication)

    def _perform_reaction(self, mle: MLE) -> Reaction:
        raise NotImplementedError()
