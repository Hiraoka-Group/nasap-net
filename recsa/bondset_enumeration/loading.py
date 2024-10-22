from dataclasses import dataclass
from pathlib import Path
from typing import Self, TypeAlias

import yaml
from pydantic import BaseModel, ConfigDict

from recsa.utils import cyclic_perms_to_map

from .validation import validate_symmetry_ops_consistency

BondId: TypeAlias = str
SymmetryOpId: TypeAlias = str


@dataclass
class Args():
    bonds: list[BondId]
    bond_to_adjs: dict[BondId, list[BondId]]
    symmetry_ops: dict[SymmetryOpId, dict[BondId, BondId]] | None


class Yamldict(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)

    bonds: list[str]
    bond_to_adjs: dict[str, list[str]]
    sym_mappings: dict[str, dict[str, str]] | None = None
    sym_perms: dict[str, list[list[str]]] | None = None


def load_bond_based_structure_data(
        filepath: str | Path
        ) -> Args:
    """Parse the input file for `translate_to_graph`."""
    filepath = Path(filepath)

    with filepath.open('r') as f:
        data = yaml.safe_load(f)

    formatted = Yamldict(**data)

    if formatted.sym_perms is None:
        return Args(
            bonds=formatted.bonds,
            bond_to_adjs=formatted.bond_to_adjs,
            symmetry_ops=formatted.sym_mappings)
    
    maps_by_perms = {
        op_id: cyclic_perms_to_map(perms)
        for op_id, perms in formatted.sym_perms.items()}

    if formatted.sym_mappings is None:
        return Args(
            bonds=formatted.bonds,
            bond_to_adjs=formatted.bond_to_adjs,
            symmetry_ops=maps_by_perms)

    validate_symmetry_ops_consistency(
        formatted.sym_mappings, maps_by_perms)
    return Args(
        bonds=formatted.bonds,
        bond_to_adjs=formatted.bond_to_adjs,
        symmetry_ops=maps_by_perms)
