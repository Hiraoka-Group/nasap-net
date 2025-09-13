# How to use

The `enumerate-assemblies` subcommand is used to enumerate assemblies.

## Syntax

```bash
nasap_net enumerate-assemblies [OPTIONS] INPUT OUTPUT
```

!!! info
    If this raises an error `command not found`, you may need to use `python -m recsa` or `python3 -m recsa` instead of `recsa`.
    ```bash
    python -m recsa enumerate-assemblies [OPTIONS] INPUT OUTPUT
    ```

### Positional Arguments
1. `INPUT`: Relative path to the input file.
2. `OUTPUT`: Relative path to the output file.

### Options
Options with single hyphen (`-`) are aliases for the corresponding options with double hyphen (`--`), e.g., `-w` is an alias for `--wip-dir`. Either of them can be used.

Command | Alias | Description | Example
--- | --- | --- | ---
`--wip-dir` | `-w` | Directory to store intermediate files. | `recsa enumerate-assemblies -w wip input.yaml output.yaml`, where `wip` is the directory to store intermediate files.
`--start` | `-s` | Starting index for the reindexing of the assemblies. | `recsa enumerate-assemblies -s 10 input.yaml output.yaml`, where the starting index in the output file is 10.
`--overwrite` | `-o` | Overwrite output file if it exists. | `recsa enumerate-assemblies -o input.yaml output.yaml`
`--verbose` | `-v` | Print feedback messages to the console. | `recsa enumerate-assemblies -v input.yaml output.yaml`
`--help` | | Show this message and exit. | `recsa enumerate-assemblies --help`

## Example

Directory structure before running the command:
```
/
└── input.yaml
```

Command:
```bash
nasap_net enumerate-assemblies input.yaml output.yaml
```

Directory structure after running the command:
```
/
├── input.yaml
└── output.yaml
```

Input and output files are as follows:

??? example "Input File"
    ``` yaml title="input.yaml"
    --8<-- "assets.h/input.yaml"
    ```

??? example "Output File"
    ``` yaml title="output.yaml"
    --8<-- "assets.h/output.yaml"
    ```

!!! note
    See [Input File](input.md) and [Output File](output.md) for more details.
