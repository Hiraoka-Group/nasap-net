# RECSA
This is the documentation for the RECSA package.

## Introduction
RECSA (Reaction Explorer for Coordination Self-Assembly) is a Python package for generating reaction networks.
Some features can be accessed through the command line interface (CLI), while others are available through the Python API.

## Installation
To install RECSA, you can use pip:
``` bash
pip install recsa
```

!!! info
    If you encounter any issues with the above command, you can try using `pip3`:

    ``` bash
    pip3 install recsa
    ```

## CLI
Some features of RECSA can be accessed through the command line interface (CLI).

### Example

``` bash
recsa enumerate-assemblies input.yaml output.yaml
```

## Python Package
RECSA can also be used as a Python package.

### Example

In the following example, we will check if two assemblies are isomorphic.
The `Assembly` objects, `MX2` and `ANOTHER_MX2`, are the same assembly but with different labels for the components and binding sites.

``` python title="example.py"
--8<-- "assets.h/isom_check_example.py"
```

1. Create an assembly object of the form X-M-X
2. Create another assembly object of the same form but with different component names
3. Define the structure of each component kind
4. Check if the two assemblies are isomorphic. This should return True, as they are structurally identical.
5. Print the result


Run the example:
``` bash
python example.py
```

Result:
``` bash
Isomorphism check: True
```
