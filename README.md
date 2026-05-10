# nasap-net

**nasap-net** is a Python library for automatically constructing elementary reaction networks within the NASAP (Numerical Analysis for Self-Assembly Process) framework, developed by the [Hiraoka Group](http://hiraoka.c.u-tokyo.ac.jp/).

## Installation

```bash
pip install nasap-net
```

Requires Python ≥ 3.12.

## What it does

Given a target assembly (a metal–organic cage) and the components that make it up, nasap-net:

1. **Enumerates all subassemblies** — finds every chemically meaningful partial structure
2. **Enumerates all elementary reactions** — generates every ligand-exchange step connecting those subassemblies
3. **Classifies reactions** — applies a user-defined rule to assign a reaction type to each elementary reaction
4. **Saves and loads results** — serializes assemblies and reactions to YAML/CSV files for downstream use

## Quick start

```python
from nasap_net import (
    Assembly, Bond, Component, MLEKind,
    enumerate_assemblies, enumerate_reactions,
    classify_reactions, IncompleteReactionClassifierError,
    save_assemblies, save_reactions, save_classification_result,
)

# Define components
M = Component(kind='M', sites=[0, 1])
L = Component(kind='L', sites=[0, 1])
X = Component(kind='X', sites=[0])

# Define target assembly
target = Assembly(
    components={'M0': M, 'M1': M, 'L0': L, 'L1': L},
    bonds=[
        Bond('M0', 1, 'L0', 0), Bond('L0', 1, 'M1', 0),
        Bond('M1', 1, 'L1', 0), Bond('L1', 1, 'M0', 0),
    ]
)

# Enumerate subassemblies and reactions
assemblies = list(enumerate_assemblies(target, leaving_ligand=X, metal_kinds='M'))
reactions = list(enumerate_reactions(
    assemblies=assemblies,
    mle_kinds=[
        MLEKind(metal='M', leaving='X', entering='L'),
        MLEKind(metal='M', leaving='L', entering='X'),
    ],
))

# Classify reactions with a user-defined rule
def my_classifier(reaction):
    reaction = reaction.as_reaction_to_classify()
    if reaction.leaving_kind == 'X' and reaction.entering_kind == 'L':
        return 'association'
    elif reaction.leaving_kind == 'L' and reaction.entering_kind == 'X':
        return 'dissociation'
    raise IncompleteReactionClassifierError(reaction)

reaction_to_class = classify_reactions(reactions, my_classifier)

# Save results
save_assemblies(assemblies, 'assemblies.yaml')
save_reactions(reactions, 'reactions.csv')
save_classification_result(reaction_to_class, 'classification_result.csv')
```

## Example

A worked example for an M4L4/M10L11 system is available as a Jupyter notebook:

[`examples/M4L4_reaction_classification/`](examples/M4L4_reaction_classification/)

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/Hiraoka-Group/nasap-net/blob/main/examples/M4L4_reaction_classification/M4L4_reaction_classification.ipynb)

## License

MIT
