"""
Debug operators for RxPy streams.

These operators help with debugging and inspecting reactive streams.
"""

import attr
from loguru import logger
from typing import Any, Callable, Optional

import reactivex
from reactivex import Observable
from reactivex.core import Observer


def debug(
    name: str = "debug",
    print_value: bool = True,
    logger_func: Callable = logger.debug
) -> Callable[[Observable], Observable]:
    """
    Debug operator for inspecting values in an observable stream.
    
    Logs the emitted values and optionally the stream events (on_completed, on_error).
    
    Args:
        name: A name to identify this debug point in logs
        print_value: Whether to print the value (might be large)
        logger_func: The logger function to use
        
    Returns:
        An operator function that returns an Observable
    """
    def _debug(source: Observable) -> Observable:
        def subscribe(observer: Observer, scheduler = None) -> reactivex.abc.DisposableBase:
            def on_next(value: Any) -> None:
                if print_value:
                    logger_func(f"{name} | on_next: {value}")
                else:
                    logger_func(f"{name} | on_next received")
                observer.on_next(value)
                
            def on_completed() -> None:
                logger_func(f"{name} | on_completed")
                observer.on_completed()
                
            def on_error(error: Exception) -> None:
                logger_func(f"{name} | on_error: {error}")
                observer.on_error(error)
                
            return source.subscribe(
                on_next=on_next,
                on_completed=on_completed,
                on_error=on_error,
                scheduler=scheduler
            )
        
        return Observable(subscribe)
    
    return _debug
