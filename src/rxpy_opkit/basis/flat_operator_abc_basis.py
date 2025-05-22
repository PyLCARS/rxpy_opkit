"""Base operator classes for flat RxPy operators.

This module provides abstract base classes for implementing RxPy operators
using a flat class structure instead of nested functions.
"""

from abc import ABC, abstractmethod
from typing import Any, Callable, Generic, Optional, TypeVar
import reactivex as rx
from reactivex import Observable
from reactivex.abc import ObserverBase, SchedulerBase, DisposableBase

# Type variables for generic typing
T = TypeVar('T')  # Input type
R = TypeVar('R')  # Result type


class BaseOperator(ABC, Generic[T, R]):
    """Abstract base class for flat RxPy operators.
    
    This class provides the common structure and interface that all
    flat class-based operators should implement. It uses the ABC module
    to enforce implementation of required methods in subclasses.
    
    Example:
        class MyOperator(BaseOperator):
            def __init__(self, transform_func):
                super().__init__()
                self.transform_func = transform_func
            
            def on_next(self, value):
                transformed = self.transform_func(value)
                self.observer.on_next(transformed)
    """
    
    def __init__(self):
        """Initialize the operator.
        
        Subclasses should override this to accept specific parameters
        and call super().__init__() to ensure proper initialization.
        """
        self.observer: Optional[ObserverBase] = None
    
    def __call__(self, source: Observable) -> Observable:
        """Make the operator callable on an observable source.
        
        This enables the operator to be used directly in a pipe:
        source.pipe(MyOperator(params))
        
        Args:
            source: The source observable
            
        Returns:
            A new observable with the operator's transformation applied
        """
        return Observable(self.subscribe_factory(source))
    
    def subscribe_factory(self, source: Observable) -> Callable:
        """Create a subscription function for the Observable constructor.
        
        Args:
            source: The source observable
            
        Returns:
            A function that takes an observer and optional scheduler
        """
        return lambda observer, scheduler=None: self.subscribe(source, observer, scheduler)
    
    def subscribe(self, 
                  source: Observable, 
                  observer: ObserverBase, 
                  scheduler: Optional[SchedulerBase] = None) -> DisposableBase:
        """Handle subscription to the source observable.
        
        This method is called when the resulting observable is subscribed to.
        It should subscribe to the source and set up the observer chain.
        
        Args:
            source: The source observable
            observer: The observer to receive notifications
            scheduler: Optional scheduler to control concurrency
            
        Returns:
            A disposable that can be used to cancel the subscription
        """
        # Store observer for use in notification handlers
        self.observer = observer
        
        # Subscribe to source and return the subscription
        return source.subscribe(
            on_next=self.on_next,
            on_error=self.on_error,
            on_completed=self.on_completed,
            scheduler=scheduler
        )
    
    @abstractmethod
    def on_next(self, value: Any) -> None:
        """Handle a value from the source observable.
        
        Subclasses MUST override this to implement their specific
        transformation logic.
        
        Args:
            value: The value from the source
        """
        raise NotImplementedError("Subclasses must implement on_next")
    
    def on_error(self, error: Exception) -> None:
        """Handle an error from the source observable.
        
        The default implementation forwards errors to the downstream observer.
        Subclasses can override this to add custom error handling.
        
        Args:
            error: The error from the source
        """
        if self.observer:
            self.observer.on_error(error)
    
    def on_completed(self) -> None:
        """Handle completion of the source observable.
        
        The default implementation forwards completion to the downstream observer.
        Subclasses can override this to add custom completion handling.
        """
        if self.observer:
            self.observer.on_completed()


class SimpleOperator(BaseOperator[T, R]):
    """Base class for operators that only transform values.
    
    This class provides a default on_next implementation that applies
    a transformation function to each value. Useful for operators like
    map, scan, etc.
    """
    
    def __init__(self, transform_func: Callable[[Any], Any]):
        """Initialize with a transformation function.
        
        Args:
            transform_func: Function to transform each value
        """
        super().__init__()
        self.transform_func = transform_func
    
    def on_next(self, value: Any) -> None:
        """Apply transformation and forward the result."""
        try:
            transformed = self.transform_func(value)
            if self.observer:
                self.observer.on_next(transformed)
        except Exception as e:
            if self.observer:
                self.observer.on_error(e)


class FilteringOperator(BaseOperator[T, T]):
    """Base class for operators that filter values.
    
    This class provides a default on_next implementation that applies
    a predicate function to each value and only forwards values that
    pass the predicate.
    """
    
    def __init__(self, predicate: Callable[[Any], bool]):
        """Initialize with a predicate function.
        
        Args:
            predicate: Function to test each value
        """
        super().__init__()
        self.predicate = predicate
    
    def on_next(self, value: Any) -> None:
        """Forward values that pass the predicate."""
        try:
            if self.predicate(value) and self.observer:
                self.observer.on_next(value)
        except Exception as e:
            if self.observer:
                self.observer.on_error(e)


class StatefulOperator(BaseOperator[T, R]):
    """Base class for operators that maintain state between emissions.
    
    This abstract class is for operators that need to maintain state
    across multiple on_next calls, like scan, buffer, distinct, etc.
    """
    
    @abstractmethod
    def reset_state(self) -> None:
        """Reset the operator's internal state.
        
        Called when the operator needs to reset its state,
        typically after completion or error.
        """
        raise NotImplementedError("Subclasses must implement reset_state")
    
    def on_completed(self) -> None:
        """Handle completion and reset state."""
        super().on_completed()
        self.reset_state()
    
    def on_error(self, error: Exception) -> None:
        """Handle error and reset state."""
        super().on_error(error)
        self.reset_state()


# Factory function helpers for traditional RxPy usage
def create_operator(operator_class: type[BaseOperator], *args, **kwargs) -> Callable:
    """Create an operator factory function for use in pipe().
    
    Args:
        operator_class: The operator class to instantiate
        *args: Positional arguments for the operator
        **kwargs: Keyword arguments for the operator
        
    Returns:
        A function that creates and applies the operator
    
    Example:
        # Instead of defining a factory function manually:
        def my_map(transform_func):
            return MyMapOperator(transform_func)
        
        # You can use:
        my_map = lambda f: create_operator(MyMapOperator, f)
    """
    def operator_factory(source: Observable) -> Observable:
        operator = operator_class(*args, **kwargs)
        return operator(source)
    return operator_factory