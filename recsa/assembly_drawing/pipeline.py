import shutil
from collections.abc import Mapping
from pathlib import Path

import matplotlib.pyplot as plt

from recsa import RecsaValueError, load_assemblies, load_component_structures
from recsa.utils import update_nested_dict

from .drawing_2d import draw_2d
from .drawing_3d import draw_3d
from .loading import load_drawing_args
from .positioning import calc_positions

__all__ = ['draw_assemblies_pipeline']


def draw_assemblies_pipeline(
        assemblies_dir: str | Path, 
        component_structures_filepath: str | Path,
        default_args_filepath: str | Path,
        output_dir: str | Path,
        id_to_custom_args_filepath: Mapping[str, str | Path] | None = None,
        overwrite: bool = False,
        **kwargs) -> None:
    """Draws the assemblies from the all the YAML files in the directory."""
    assemblies_dir = Path(assemblies_dir)
    default_args_filepath = Path(default_args_filepath)
    if id_to_custom_args_filepath is None:
        id_to_custom_args_filepath = {}
    else:
        id_to_custom_args_filepath = {
            assem_id: Path(filepath)
            for assem_id, filepath in id_to_custom_args_filepath.items()}
    
    # Read assemblies
    id_assem_pairs = load_assemblies(assemblies_dir)
    # Read component structures
    component_structures = load_component_structures(
        component_structures_filepath)

    # Read drawing parameters
    default_drawing_args = load_drawing_args(default_args_filepath)

    # Create output folder
    output_dir_obj = Path(output_dir)

    if output_dir_obj.exists() and not overwrite:
        raise RecsaValueError(
            f'The output directory {output_dir_obj} already exists. '
            'Set the overwrite flag to True to overwrite the directory.')
    elif output_dir_obj.exists() and overwrite:
        shutil.rmtree(output_dir_obj)
    output_dir_obj.mkdir(parents=True, exist_ok=True)

    # Plot graphs
    for assem_id, assem in id_assem_pairs:
        drawing_args = default_drawing_args
        if assem_id in id_to_custom_args_filepath:

            custom_args = load_drawing_args(
                id_to_custom_args_filepath[assem_id])
            drawing_args = update_nested_dict(drawing_args, custom_args)

        drawing_args = update_nested_dict(drawing_args, kwargs)
        
        dimensions = drawing_args.get('dimensions', '2d')
        output_format = drawing_args.get('output_format', 'pdf')
        
        if 'positioning_args' in drawing_args:
            positioning_args = drawing_args['positioning_args']
            pos = calc_positions(
                assem, component_structures, dimensions=dimensions,
                layout_name=positioning_args['layout'],
                init_pos=positioning_args.get('init_pos', None),
                fixed=positioning_args.get('fixed', None),
                other_layout_kwargs=positioning_args.get('other_args', {}))
        else:
            pos = calc_positions(
                assem, component_structures, dimensions=dimensions)

        match dimensions:
            case '2d':
                draw_2d(
                    assem, component_structures, pos,
                    show=False, **drawing_args['draw_2d_args'])
            case '3d':
                draw_3d(
                    assem, component_structures, pos,
                    show=False, **drawing_args['draw_3d_args'])
        
        output_filepath = output_dir_obj / f'{assem_id}.{output_format}'
        plt.savefig(output_filepath)
        print(f'Saved ---> {output_filepath}')

        plt.close()
