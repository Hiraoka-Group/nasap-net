from pathlib import Path

__all__ = ['save_duplicates_info']


def save_duplicates_info(
        unique_id_to_duplicates: dict[str, set[str]],
        output_path: str,
        overwrite: bool | None = None) -> None:
    """Save duplicates information."""
    path_obj = Path(output_path)
    if path_obj.exists():
        if overwrite is None:
            overwrite = input(
                'Output folder already exists. Overwrite? (y/n): ') == 'y'
        if overwrite:
            path_obj.unlink()
        else:
            print('Canceled.')
            return

    filtered_unique_id_to_duplicates = {
        u: d for u, d in unique_id_to_duplicates.items() if len(d) > 1}

    with open(path_obj, 'w') as f:
        if not filtered_unique_id_to_duplicates:
            f.write('No duplicates found.\n')
            return
        f.write('Removed duplicates\n')
        f.write('(unique_id): (duplicate1), (duplicate2), ...\n')
        f.write('------------------------------\n')
        for unique_id, duplicates in unique_id_to_duplicates.items():
            f.write(f'{unique_id}: {", ".join(sorted(duplicates))}\n')
    print(f'Saved! ---> "{path_obj}"')
