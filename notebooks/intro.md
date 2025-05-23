# RxPy OpKit: Enhanced Operators for Reactive Programming

Welcome to the documentation for RxPy OpKit, a library that extends [RxPy](https://rxpy.readthedocs.io/) with custom operators and utilities for reactive programming.

## What is RxPy OpKit?

RxPy OpKit provides a collection of enhanced operators for reactive programming with RxPy, focusing on:

1. **Flat Class Operators**: A more intuitive and maintainable approach to creating custom operators
2. **Logging Operators**: Rich, contextual logging capabilities using loguru
3. **Missing Operators**: Implementation of operators found in other Rx libraries but missing from RxPy

## Why RxPy OpKit?

Traditional RxPy operators use nested functions, which can be difficult to read, test, and maintain. RxPy OpKit introduces a flat class structure for operators that simplifies development while preserving all the power of reactive programming.

```python
# Traditional RxPy operator (nested functions)
def traditional_operator(param):
    def _(source):
        def subscribe(observer, scheduler=None):
            def on_next(value):
                # Process value
                observer.on_next(processed)
            # More nested functions...
            return source.subscribe(on_next, on_error, on_completed, scheduler)
        return rx.create(subscribe)
    return _

# RxPy OpKit flat class structure
class FlatOperator(BaseOperator):
    def __init__(self, param):
        super().__init__()
        self.param = param
    
    def on_next(self, value):
        # Process value
        self.observer.on_next(processed)
    
    # Other methods...
```

## How to Use This Documentation

This documentation is organized into several sections:

- **Flat Operators**: Explains the rationale and implementation of the flat class structure
- **Logging**: Demonstrates how to use the logging operators for debugging and monitoring
- **Missing Operators**: Documents additional operators that extend RxPy's capabilities
- **Testing**: Provides guidance on testing reactive code using the library

## Getting Started

To get started with RxPy OpKit, you'll need to install the package:

```bash
# Clone the repository
git clone https://github.com/GProtoZeroW/rxpy_opkit.git
cd rxpy_opkit

# Create a virtual environment with pyenv
pyenv virtualenv 3.13.1 rxpy_opkit
pyenv local rxpy_opkit

# Install in development mode
pip install -e .
```

## Interactive Examples

Throughout this documentation, you'll find interactive examples in Jupyter notebooks that demonstrate how to use the library's features.

```{note}
This documentation is a work in progress and will be expanded as the library evolves.
```
