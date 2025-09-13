# `--wip-dir` Option

The `--wip-dir` option (alias `-w`) is used to specify the directory to store intermediate files. This option is useful for debugging and determining the cause of errors during the assembly enumeration process.

## Example

If you want to store intermediate files in a directory named `wip`, run the following command:

```bash
nasap_net enumerate-assemblies --wip-dir wip input.yaml output.yaml
```

After running the command, the directory structure will be as follows:

```
/
├── input.yaml
├── output.yaml
└── wip
    ├── resolved_sym_ops.yaml
    ├── wip1_bondsets.yaml
    ├── wip2_assemblies.yaml
    ├── wip3_unique_assemblies.yaml
    └── wip4_capped_assemblies.yaml
```

## Files
### `resolved_sym_ops.yaml` file
Contains resolved symmetry operations.
All symmetry operations are represented as a mapping of the bond IDs.
Use this file to check if the symmetry operations are resolved correctly.

???+ example "resolved_sym_ops.yaml"
    ``` yaml
    --8<-- "assets.h/wip/resolved_sym_ops.yaml"
    ```

??? example "`sym_ops` field in the input file which is used to resolve the symmetry operations."
    You can see all the symmetry operations in the `sym_ops` field of the input file (below) are resolved and represented as a mapping in the `resolved_sym_ops.yaml` file (above).
    ``` yaml
    sym_ops:
    C_4: [[1, 3, 5, 7], [2, 4, 6, 8]]
    C_2: [[1, 5], [2, 6], [3, 7], [4, 8]]
    C_4^3: [[1, 7, 5, 3], [2, 8, 6, 4]]
    C_2x: [[1, 2], [3, 8], [4, 7], [5, 6]]
    C_2y: [[1, 6], [2, 5], [3, 4], [7, 8]]
    C_2(1): [[1, 4], [2, 3], [5, 8], [6, 7]]
    C_2(2): [[1, 8], [2, 7], [3, 6], [4, 5]]
    ```

---
### `wip1_bondsets.yaml` file
Contains fragments of the given assembly represented as lists of bond IDs.

???+ example "wip1_bondsets.yaml"
    ``` yaml
    --8<-- "assets.h/wip/wip1_bondsets.yaml"
    ```

---
### `wip2_assemblies.yaml` file
Contains assembly objects converted from the bond sets.

???+ example "wip2_assemblies.yaml"
    ``` yaml
    --8<-- "assets.h/wip/wip2_assemblies.yaml"
    ```

---
### `wip3_unique_assemblies.yaml` file
Contains unique assemblies.

???+ example "wip3_unique_assemblies.yaml"
    ``` yaml
    --8<-- "assets.h/wip/wip3_unique_assemblies.yaml"
    ```

---
### `wip4_capped_assemblies.yaml` file
Contains capped assemblies.

???+ example "wip4_capped_assemblies.yaml"
    ``` yaml
    --8<-- "assets.h/wip/wip4_capped_assemblies.yaml"
    ```


