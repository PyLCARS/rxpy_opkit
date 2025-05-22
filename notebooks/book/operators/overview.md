# Operators Overview

RxPy OpKit provides a collection of operators that extend the capabilities of the RxPy library.

## What are Operators?

In reactive programming, operators are functions that take an Observable as input and return a new Observable. They allow you to transform, filter, combine, and manipulate streams of data in various ways.

## Categories of Operators

RxPy OpKit organizes operators into several categories:

### Basic Operators

These are fundamental operators that provide common transformations and operations:

- Data transformation
- Filtering
- Combining streams
- Error handling

### Logging Operators

Specialized operators for debugging and monitoring reactive streams:

- Value logging
- Error logging
- Completion logging
- Performance monitoring

### Custom Operators

Domain-specific operators for particular use cases:

- State management
- Caching
- Retry strategies
- Backpressure handling

## Using Operators

Operators in RxPy OpKit follow the same pattern as standard RxPy operators. They can be used with the `pipe()` method:

```python
import reactivex as rx
from reactivex import operators as ops
from rxpy_opkit.operators import custom_op

# Create an observable
source = rx.of(1, 2, 3, 4, 5)

# Apply operators
result = source.pipe(
    ops.map(lambda x: x * 10),  # Standard RxPy operator
    custom_op(param="value")    # Custom operator from OpKit
)

# Subscribe to see results
result.subscribe(
    on_next=lambda x: print(f"Value: {x}"),
    on_completed=lambda: print("Completed")
)
```
