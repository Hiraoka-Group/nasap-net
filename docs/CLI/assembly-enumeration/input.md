# Input File

## Table of Contents

- [Example](#example)
- [Fields](#fields)

## Example

--8<-- "about-example.h.md"

``` yaml title="input.yaml"
--8<-- "assets.h/input.yaml"
```

Download the example input file: [input.yaml](assets.h/input.yaml){:download}

## Fields

### `bonds` field

``` yaml
bonds: [1, 2, 3, 4, 5, 6, 7, 8]
```

A list of bond IDs.

- IDs must be unique. (**Incorrect**: `[1, 1, 2]`)
- IDs can be either integers or strings. (Correct: `1`, `a`, `bond1`, `"1"`)
- ID type must be consistent. (**Incorrect**: `[1, "a"]`)

---
### `bond_adjacency` field

``` yaml
bond_adjacency:
  1: [8, 2]
  2: [1, 3]
  3: [2, 4]
  4: [3, 5]
  5: [4, 6]
  6: [5, 7]
  7: [6, 8]
  8: [7, 1]
```

A dictionary where keys are bond IDs and values are lists of adjacent bond IDs.

For example, `#!yaml 1: [8, 2]` means that bond 1 is adjacent to bonds 8 and 2.

---
### `sym_ops` field

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

A dictionary where keys are symmetry operation names and values are symmetry operation definitions.

Names of symmetry operations can be any string.

Three types of definitions are supported:

#### 1. Permutation of bond IDs
``` yaml
C_4: [[1, 3, 5, 7], [2, 4, 6, 8]]
```
This means that the symmetry operation `C_4` maps 1 to 3, 3 to 5, 5 to 7, and 7 to 1. Similarly, 2 to 4, 4 to 6, 6 to 8, and 8 to 2.

!!! note
    If there are bonds that do not move, represent them as a list containing only one element, like this:

    ``` yaml
    sigma_x: [[1], [2, 3]]
    ```

    This means that the symmetry operation `sigma_x` maps 1 to 1, 2 to 3, and 3 to 2, i.e., 1 remains at the same position.

#### 2. Mapping of bond IDs: 
``` yaml
C_4: {1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8, 7: 1, 8: 2}
```

Symmetry operations can also be defined as a dictionary where keys are bond IDs and values are the bond IDs to which they are mapped.

#### 3. Composition of other symmetry operations: 
``` yaml
C_2y: [C_2x, C_2]
```

Symmetry operations can be defined as a product of other symmetry operations. In this case, `C_2y` is defined as the composition of `C_2x` and `C_2`.

!!! warning
    The order of the symmetry operations in the composition is important. The symmetry operation on the right is applied first. For example, `C_2y` is defined as `C_2` followed by `C_2x`.

!!! note
    Composition of three or more symmetry operations is also supported. For example:
    ``` yaml
    C_4^3: [C_4, C_4, C_4]
    ```

#### Combination of representation types

The representation types can be mixed in the `sym_ops` field. For example:
``` yaml
sym_ops:
  C_4: [[1, 3, 5, 7], [2, 4, 6, 8]]  # Permutation
  C_2: [C_4, C_4]  # Composition
  C_4^3: {1: 7, 2: 8, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6}  # Mapping
  C_2x: [[1, 2], [3, 8], [4, 7], [5, 6]]
  C_2y: [C_2x, C_2]
  C_2(1): [C_4, C_2x]
  C_2(2): [C_2x, C_4]
```

---
### `component_kinds` field

``` yaml
component_kinds:
  L: !Component
    binding_sites: [a, b]
  M: !Component
    binding_sites: [a, b]
  X: !Component
    binding_sites: [a]
```

A dictionary where keys are names of component kinds and values are component definitions.

!!! note
    Component kinds can also have "auxiliary edges" defined. For example:
    ``` yaml
    component_kinds:
      M: !Component
        binding_sites: [a, b, c, d]
        aux_edges: [[a, b, cis], [b, c, cis], [c, d, cis], [d, a, cis]]
    ```
    The auxiliary edges can be used to define the relative orientation of the binding sites in the component, which can be used to distinguish between different stereoisomers.

---
### `components_and_their_kinds` field

``` yaml
components_and_their_kinds:
  M1: M
  M2: M
  M3: M
  M4: M
  L1: L
  L2: L
  L3: L
  L4: L
```

A dictionary where keys are component names and values are component kind names defined in the `component_kinds` field.

---
### `bonds_and_their_binding_sites` field

``` yaml
bonds_and_their_binding_sites:
  1: [M1.b, L1.a]
  2: [L1.b, M2.a]
  3: [M2.b, L2.a]
  4: [L2.b, M3.a]
  5: [M3.b, L3.a]
  6: [L3.b, M4.a]
  7: [M4.b, L4.a]
  8: [L4.b, M1.a]
```

A dictionary where keys are bond IDs and values are lists of binding sites.
For example, `#!yaml 1: [M1.b, L1.a]` means that bond 1 connects the binding site `b` of component `M1` to the binding site `a` of component `L1`.
Here, `M1.b` refers to the binding site `b` of component `M1`.

---
### `capping_config` field

``` yaml
capping_config:
  target_component_kind: M
  capping_component_kind: X
  capping_binding_site: a
```

A dictionary that defines the capping configuration.

- `target_component_kind`: The component kind to be capped.
- `capping_component_kind`: The component kind to be used for capping.
- `capping_binding_site`: The binding site of the capping component to be connected to the target component.
