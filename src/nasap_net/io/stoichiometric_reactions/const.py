from enum import Enum


class Column(Enum):
    """Column names for reaction data."""
    REACTANT1 = 'reactant1'
    REACTANT2 = 'reactant2'
    PRODUCT1 = 'product1'
    PRODUCT2 = 'product2'
    DUPLICATE_COUNT = 'duplicate_count'
    ID_ = 'id'
