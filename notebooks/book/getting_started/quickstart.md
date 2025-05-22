# Quickstart

This guide will help you get started with RxPy OpKit quickly.

## Basic Usage

Here's a simple example of using a debug operator from RxPy OpKit:

```python
import reactivex as rx
from reactivex import operators as ops
from loguru import logger

# Import the debug operator from rxpy_opkit
from rxpy_opkit.operators.debug_operators import debug

# Create a simple observable
source = rx.of(1, 2, 3, 4, 5)

# Use the debug operator to log values
result = source.pipe(
    ops.map(lambda x: x * 10),
    debug(name="after_map"),  # Log values after map
    ops.filter(lambda x: x > 20),
    debug(name="after_filter")  # Log values after filter
)

# Subscribe to see the results
result.subscribe(
    on_next=lambda x: logger.info(f"Final value: {x}"),
    on_completed=lambda: logger.info("Completed")
)
```

## Creating Custom Operators

You can create your own operators following this pattern:

```python
import attr
from typing import Callable, Any
import reactivex
from reactivex import Observable
from reactivex.core import Observer
from loguru import logger

def my_custom_operator(param: Any = None) -> Callable[[Observable], Observable]:
    """
    A custom operator that does something useful.
    
    Args:
        param: An optional parameter
        
    Returns:
        An operator function that returns an Observable
    """
    def _operator(source: Observable) -> Observable:
        def subscribe(observer: Observer, scheduler = None) -> reactivex.abc.DisposableBase:
            def on_next(value: Any) -> None:
                # Process the value
                processed_value = do_something_with(value, param)
                observer.on_next(processed_value)
                
            def on_completed() -> None:
                # Handle completion
                observer.on_completed()
                
            def on_error(error: Exception) -> None:
                # Handle error
                observer.on_error(error)
                
            return source.subscribe(
                on_next=on_next,
                on_completed=on_completed,
                on_error=on_error,
                scheduler=scheduler
            )
        
        return Observable(subscribe)
    
    return _operator

def do_something_with(value, param):
    # Your custom logic here
    return value
```

## Using Logging Operators

RxPy OpKit provides specialized logging operators:

```python
from rxpy_opkit.logging import log_next, log_error, log_completed

# Create an observable with logging
rx.of(1, 2, 3).pipe(
    log_next("Emitted value: {}"),
    ops.map(lambda x: x * 10),
    log_next("After map: {}"),
    log_completed("Stream completed")
).subscribe()
```
