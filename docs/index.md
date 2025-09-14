# NASAPNet
This is the documentation for NASAPNet.

## Introduction
NASAPNet is a Python package that automates the construction of reaction networks as part of the NASAP (Numerical Analysis for Self-Assembly Process) methodology, originally developed by the Hiraoka Group. NASAPNet is designed to streamline and accelerate the process of generating reaction networks for self-assembly systems, and is one of several tools in the NASAP series.

Some features can be accessed through the command line interface (CLI), while others are available through the Python API.

## Installation
To install NASAPNet, you can use pip:
``` bash
pip install nasap_net
```

!!! info
    If you encounter any issues with the above command, you can try using `pip3`:

    ``` bash
    pip3 install nasap_net
    ```

## CLI
Some features of NASAPNet can be accessed through the command line interface (CLI).

### Example

``` bash
nasapnet enumerate-assemblies input.yaml output.yaml
```

## Python Package
NASAPNet can also be used as a Python package, e.g., `import nasap_net`.

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
