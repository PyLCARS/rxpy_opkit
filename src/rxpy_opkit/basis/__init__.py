"""Basis module for RxPy OpKit - Foundation classes for building operators.

This module provides the abstract base classes and core implementations
for building custom RxPy operators using a flat class structure.
"""

from .flat_operator_abc_basis import (
    # Abstract base classes
    BaseOperator,
    StatefulOperator,
    
    # Concrete base implementations
    SimpleOperator,
    FilteringOperator,
    
    # Helper functions
    create_operator,
    
    # Type variables (for type hints)
    T,
    R,
)

__all__ = [
    # Core ABCs
    "BaseOperator",
    "StatefulOperator",
    
    # Implementations
    "SimpleOperator",
    "FilteringOperator",
    
    # Utilities
    "create_operator",
    
    # Types
    "T",
    "R",
]

__version__ = "0.1.0"