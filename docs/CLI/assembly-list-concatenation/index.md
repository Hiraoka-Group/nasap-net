# How to use

The `concat-assembly-lists` subcommand is used to concatenate assembly lists.
The assemblies in the input files are concatenated and reindexed. 

The command will check for isomorphism between assemblies, and isomorphic assemblies will be merged (unless the `--skip-isomorphism-checks` option is used).

## Syntax

```bash
nasap_net concat-assembly-lists [OPTIONS] [ASSEMBLIES]... COMPONENT_KINDS OUTPUT
```

!!! info
    If this raises an error `command not found`, you may need to use `python -m recsa` or `python3 -m recsa` instead of `recsa`.
    ```bash
    python -m recsa concat-assembly-lists [OPTIONS] [ASSEMBLIES]... COMPONENT_KINDS OUTPUT
    ```

### Positional Arguments
1. `ASSEMBLIES`: Paths to input files of assemblies. Multiple paths can be provided.
2. `COMPONENT_KINDS`: Path to input file of component kinds.
3. `OUTPUT`: Path to output file.

### Options
- `--already-unique-within-files`, `-u`: Whether the assemblies in each file are already unique. If used, the isomorphism checks are skipped for the assemblies within each file.
- `--skip-isomorphism-checks`, `-i`: Skip isomorphism checks for the assemblies. If used, the isomorphism checks are skipped for all assemblies. The resulting assembly list may contain isomorphic assemblies.
- `--start`, `-s`: Starting index for the reindexing of the assemblies.
- `--overwrite`, `-o`: Overwrite output file if it exists.
- `--verbose`, `-v`: Print verbose output.
- `--help`: Show this message and exit.

## Example

Directory structure before running the command:
```
/
├── assemblies1.yaml
├── assemblies2.yaml
└── component_kinds.yaml
```

Command:
```bash
nasap_net concat-assembly-lists assemblies1.yaml assemblies2.yaml component_kinds.yaml output.yaml
```

Directory structure after running the command:
```
/
├── assemblies1.yaml
├── assemblies2.yaml
├── component_kinds.yaml
└── output.yaml
```

Input and output files are as follows:

??? example "Input File"
    ``` yaml title="assemblies1.yaml"
    --8<-- "assets.h/assemblies1.yaml"
    ```

??? example "Input File"
    ``` yaml title="assemblies2.yaml"
    --8<-- "assets.h/assemblies2.yaml"
    ```

??? example "Output File"
    ``` yaml title="output.yaml"
    --8<-- "assets.h/output.yaml"
    ```
