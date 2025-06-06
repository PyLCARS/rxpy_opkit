# RxPy OpKit

[![Documentation](https://github.com/PyLCARS/rxpy_opkit/actions/workflows/deploy-book.yml/badge.svg)](https://pylcars.github.io/rxpy_opkit/intro.html)
[![Tests](https://github.com/PyLCARS/rxpy_opkit/actions/workflows/run-tests.yml/badge.svg)](https://github.com/PyLCARS/rxpy_opkit/actions/workflows/run-tests.yml)

A collection of custom operators and tools for RxPy using flat class structure, including logging, debugging, and missing operators from other Rx implementations.

📚 **[View the Documentation](https://pylcars.github.io/rxpy_opkit/intro.html)**

## Overview

RxPy OpKit provides a foundation for building reactive applications with improved operator ergonomics. The library focuses on:

1. **Basis Classes**: Abstract base classes for creating custom RxPy operators using a flat class structure
2. **Logging Operators**: Rich, structured logging using loguru for debugging reactive streams using our flat class structure
3. **Extended Operators**: Implementations of operators missing from RxPy but present in other Rx implementations

## Installation

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

For development dependencies:

```bash
pip install -e ".[dev]"
```

## Core Components

### Basis Module

The `basis` module provides the foundation classes for building operators:

```python
from rxpy_opkit.basis import BaseOperator, StatefulOperator, SimpleOperator

# Create a custom operator
class MyCustomOperator(BaseOperator):
    def __init__(self, param):
        super().__init__()
        self.param = param
        
    def on_next(self, value):
        result = process_value(value, self.param)
        self.observer.on_next(result)
```

### Logging Operators

The `logging_ops` module provides rich logging capabilities using loguru:

```python
import reactivex as rx
from reactivex import operators as ops
from rxpy_opkit import log, marble_log, perf_log

# Create a simple observable with logging
rx.of(1, 2, 3, 4, 5).pipe(
    log("Source"),
    ops.map(lambda x: x * 10),
    marble_log("Marble"),
    perf_log("Performance")
).subscribe()
```

## Key Features

### Flat Class Structure

Unlike traditional RxPy operators that use nested functions, RxPy OpKit uses a flat class structure for better readability, testability, and reusability:

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

### Rich Logging

RxPy OpKit provides multiple logging options:

- `LoggingOperator`: Basic logging of values, errors, and completion
- `MarbleLogger`: ASCII marble diagram-style logs
- `ContextualLogger`: Logs with stream context
- `RichLoggerOperator`: Formatted logging with colors
- `PerformanceLogger`: Tracks timing and throughput
- `ConditionalLogger`: Logs based on predicates

### Factory Functions

For convenience, factory functions are provided for all logging operators:

```python
from rxpy_opkit import log, marble_log, context_log, rich_log, perf_log, conditional_log

# Use in a pipe
source.pipe(
    log("Basic"),
    marble_log("Marble"),
    # More operators...
)
```

## Development

### Running Tests
**TODO**

```bash
pytest
```

### Documentation

The project documentation is built with Jupyter Book:

```bash
# Install docs dependencies
pip install -e ".[dev]"

# Build the docs
jupyter-book build notebooks

# View the docs locally
open notebooks/_build/html/index.html

# Online documentation
# The documentation is available at: https://pylcars.github.io/rxpy_opkit/intro.html
```

## License

RxPy OpKit is released under the MIT License. See the [LICENSE](./LICENSE) file for details.

```
MIT License
Copyright (c) 2025 GProtoZeroW
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch: `git checkout -b feature/amazing-feature`
3. Commit your changes: `git commit -m '[checkpoint] Add some amazing feature'`
4. Push to the branch: `git push origin feature/amazing-feature`
5. Open a Pull Request

## Contributors

- GProtoZeroW
