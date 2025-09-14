# How to use

The `explore-reactions` subcommand is used to explore reactions between assemblies.

## Syntax

```bash
nasapnet explore-reactions [OPTIONS] ASSEMBLIES COMPONENT_KINDS CONFIG OUTPUT
```

!!! info
    If this raises an error `command not found`, you may need to use `python -m nasap_net` or `python3 -m nasap_net` instead of `nasapnet`.
    ```bash
    python -m nasap_net explore-reactions [OPTIONS] ASSEMBLIES COMPONENT_KINDS CONFIG OUTPUT
    ```

### Positional Arguments
1. `ASSEMBLIES`: Relative path to the assemblies file. (YAML format)
2. `COMPONENT_KINDS`: Relative path to the component kinds file. (YAML format)
3. `CONFIG`: Relative path to the config file. (YAML format)
4. `OUTPUT`: Relative path to the output file. (CSV format)

### Options
Options with single hyphen (`-`) are aliases for the corresponding options with double hyphen (`--`), e.g., `-w` is an alias for `--wip-dir`. Either of them can be used.

Command | Alias | Description | Example
--- | --- | --- | ---
`--overwrite` | `-o` | Overwrite output file if it exists. | `nasapnet explore-reactions -o input.yaml output.yaml`
`--verbose` | `-v` | Print feedback messages to the console. | `nasapnet explore-reactions -v input.yaml output.yaml`
`--help` | | Show this message and exit. | `nasapnet explore-reactions --help`

!!! warning "Reversible reactions not guaranteed"
    The `explore-reactions` command considers left-to-right and right-to-left reactions as separate reactions.
    
    This means that the results may contain only one direction of a reversible reaction. 
    
    ---
    For example, if the config file is set up as follows:
    ```yaml
    mle_kinds: 
        metal_kind: M
        leaving_kind: X
        reactant_kind: L
    ```
    the results only include "X-to-L" reactions, **NOT** "L-to-X".

    e.g., "MX4 + L -> MX3L + X" will be included, but the reverse "MX3L + X -> MX4 + L" will never be included.
    
    If you want to include both directions, you can run the command twice with swapped `reactant_kind` and `leaving_kind` in the config file,
    e.g.,
    ```yaml
    mle_kinds: 
        metal_kind: M
        leaving_kind: L
        reactant_kind: X
    ```
    This will include "L-to-X" reactions, such as "MX3L + X -> MX4 + L".

    Then you can concatenate the two resulting CSV files.

## Example

Directory structure before running the command:
```
/
├── assemblies.yaml
├── component_kinds.yaml
└── config.yaml
```

Command:
```bash
nasapnet explore-reactions assemblies.yaml component_kinds.yaml config.yaml output.csv
```

Directory structure after running the command:
```
/
├── assemblies.yaml
├── component_kinds.yaml
├── config.yaml
└── output.csv
```

Input and output files are as follows:

??? example "Input File (1) assemblies.yaml"
    ``` yaml title="assemblies.yaml"
    --8<-- "assets.h/assemblies.yaml"
    ```

??? example "Input File (2) component_kinds.yaml"
    ``` yaml title="component_kinds.yaml"
    --8<-- "assets.h/component_kinds.yaml"
    ```

??? example "Input File (3) config.yaml"
    ``` yaml title="config.yaml"
    --8<-- "assets.h/config.yaml"
    ```

??? example "Output File"
    !!! warning
        The output file only contains the X-to-L reactions, not the L-to-X reactions.
    {{ read_csv('assets.h/output.csv') }}