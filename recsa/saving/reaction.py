import shutil
from collections.abc import Iterable
from pathlib import Path

import yaml

from recsa.classes.reaction import InterReaction, IntraReaction
from recsa.saving.utils.reaction_namings_archives import generate_reaction_name

from .representers.reaction import add_reaction_representer

__all__ = ['save_reactions', 'save_reaction']


add_reaction_representer()


def save_reaction(
        reaction: IntraReaction | InterReaction,
        filepath: str | Path,
        overwrite: bool = False,
        ) -> None:
    filepath = Path(filepath)

    if filepath.exists() and not overwrite:
        raise FileExistsError(f'{filepath} already exists')
    with open(filepath, 'w') as f:
        yaml.dump(reaction, f)


def save_reactions(
        reactions: Iterable[IntraReaction | InterReaction],
        output_dir: str | Path,
        overwrite_dir: bool = False,
        ) -> None:
    output_dir = Path(output_dir)

    if output_dir.exists():
        if overwrite_dir:
            shutil.rmtree(output_dir)
        else:
            raise FileExistsError(f'{output_dir} already exists')
        
    output_dir.mkdir(parents=True)

    for i, reaction in enumerate(reactions):
        name = generate_reaction_name(reaction)
        output_path = output_dir / f'{name}.yaml'
        with open(output_path, 'w') as f:
            yaml.dump(reaction, f)
