"""Logging and debugging operators for RxPy streams.

This module provides various operators for logging, debugging, and monitoring
reactive streams using Loguru for rich, structured logging.
"""

import time
import sys
from typing import Any, Callable, Optional, Dict, List, Union

import reactivex as rx
from reactivex import Observable
from reactivex import operators as ops
from loguru import logger

# Import base classes from basis module
from ..basis import BaseOperator, StatefulOperator, T

# Configure default logger - users can reconfigure as needed
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    colorize=True,
    level="INFO",
    diagnose=False,
    backtrace=False
)


class LoggingOperator(BaseOperator[T, T]):
    """A dedicated operator for logging events in a reactive stream using Loguru."""
    
    def __init__(self, 
                 prefix: str = "RxLog",
                 log_values: bool = True,
                 log_errors: bool = True,
                 log_completion: bool = True,
                 log_level: str = "INFO",
                 value_formatter: Optional[Callable[[Any], str]] = None):
        """Initialize with logging configuration.
        
        Args:
            prefix: Prefix for log messages
            log_values: Whether to log values (on_next events)
            log_errors: Whether to log errors (on_error events)
            log_completion: Whether to log completion (on_completed events)
            log_level: Logging level to use
            value_formatter: Optional custom formatter for values
        """
        super().__init__()
        self.prefix = prefix
        self.log_values = log_values
        self.log_errors = log_errors
        self.log_completion = log_completion
        self.log_level = log_level.lower()
        self.value_formatter = value_formatter or self._default_format_value
        self.count = 0
    
    def on_next(self, value: T) -> None:
        """Log and forward the value."""
        if self.log_values:
            self.count += 1
            log_func = getattr(logger, self.log_level)
            formatted_value = self.value_formatter(value)
            log_func(f"[{self.prefix}] [{self.count}] Value: {formatted_value}")
        self.observer.on_next(value)
    
    def on_error(self, error: Exception) -> None:
        """Log and forward the error."""
        if self.log_errors:
            logger.error(f"[{self.prefix}] Error: {type(error).__name__}: {str(error)}")
        self.observer.on_error(error)
    
    def on_completed(self) -> None:
        """Log and forward completion."""
        if self.log_completion:
            logger.info(f"[{self.prefix}] Completed after {self.count} values")
        self.observer.on_completed()
    
    def _default_format_value(self, value: Any) -> str:
        """Default formatter for values, handling large values gracefully."""
        if isinstance(value, dict):
            return str(dict(list(value.items())[:5])) + (f"... ({len(value)} items)" if len(value) > 5 else "")
        elif isinstance(value, (list, tuple)) and len(value) > 5:
            return f"{value[:5]} ... ({len(value)} items)"
        else:
            s = str(value)
            return s[:97] + "..." if len(s) > 100 else s


class MarbleLogger(BaseOperator[T, T]):
    """Creates ASCII marble diagram-style logs for reactive streams."""
    
    def __init__(self, name: str, width: int = 40):
        """Initialize with diagram configuration.
        
        Args:
            name: Name of the stream (shown on the left)
            width: Width of the timeline in characters
        """
        super().__init__()
        self.name = name
        self.width = width
        self.timeline = []
        logger.info(f"{self.name.rjust(15)}: {'-' * self.width} (START)")
    
    def on_next(self, value):
        """Add value to timeline and print."""
        self.timeline.append(("N", value))
        self._print_timeline()
        self.observer.on_next(value)
    
    def on_error(self, error):
        """Add error to timeline and print."""
        self.timeline.append(("E", error))
        self._print_timeline(f"ERROR: {type(error).__name__}")
        self.observer.on_error(error)
    
    def on_completed(self):
        """Add completion to timeline and print."""
        self.timeline.append(("C", None))
        self._print_timeline("COMPLETED")
        self.observer.on_completed()
    
    def _print_timeline(self, suffix: str = ""):
        """Print the current timeline with marble diagram symbols."""
        timeline_chars = list("-" * self.width)
        
        # Map recent events to symbols on the timeline
        recent_events = self.timeline[-self.width:]
        for i, (event_type, value) in enumerate(recent_events):
            pos = i % self.width
            
            if event_type == "N":
                if isinstance(value, (int, float)) and -9 <= value <= 9:
                    symbol = str(int(value))
                elif isinstance(value, str) and value:
                    symbol = value[0].upper()
                else:
                    symbol = "•"
            elif event_type == "E":
                symbol = "X"
            elif event_type == "C":
                symbol = "|"
            else:
                symbol = "-"
            
            timeline_chars[pos] = symbol
        
        timeline = "".join(timeline_chars)
        marble_message = f"{self.name.rjust(15)}: {timeline}"
        if suffix:
            marble_message += f" ({suffix})"
        logger.info(marble_message)


class ContextualLogger(BaseOperator[T, T]):
    """Logs with context about the stream's state and history using Loguru."""
    
    def __init__(self, name: str, context: Optional[Dict[str, Any]] = None):
        """Initialize with context information.
        
        Args:
            name: Name for this logger instance
            context: Optional dict of context values to include in all logs
        """
        super().__init__()
        self.name = name
        self.context = context or {}
        self.event_count = 0
        self.start_time = time.time()
        self.log = logger.bind(operator=name, **self.context)
    
    def on_next(self, value):
        """Log value with context."""
        self.event_count += 1
        elapsed = time.time() - self.start_time
        
        self.log.bind(
            event="on_next",
            count=self.event_count,
            elapsed_sec=round(elapsed, 3),
            value_type=type(value).__name__
        ).info(f"Value: {value}")
        
        self.observer.on_next(value)
    
    def on_error(self, error):
        """Log error with context."""
        elapsed = time.time() - self.start_time
        
        self.log.bind(
            event="on_error",
            count=self.event_count,
            elapsed_sec=round(elapsed, 3),
            error_type=type(error).__name__
        ).error(f"Error: {error}")
        
        self.observer.on_error(error)
    
    def on_completed(self):
        """Log completion with context."""
        elapsed = time.time() - self.start_time
        
        self.log.bind(
            event="on_completed",
            count=self.event_count,
            elapsed_sec=round(elapsed, 3)
        ).info("Completed")
        
        self.observer.on_completed()


class RichLoggerOperator(BaseOperator[T, T]):
    """Demonstrates Loguru's rich formatting capabilities for RxPy streams."""
    
    def __init__(self, name: str, colorize: bool = True, show_type: bool = True):
        """Initialize with formatting options.
        
        Args:
            name: Name for the logger
            colorize: Whether to use colors in output
            show_type: Whether to show value types
        """
        super().__init__()
        self.name = name
        self.colorize = colorize
        self.show_type = show_type
        self.count = 0
    
    def on_next(self, value):
        """Log value with rich formatting."""
        self.count += 1
        
        # Format based on value type
        if isinstance(value, dict):
            self._log_dict(value)
        elif isinstance(value, (list, tuple)):
            self._log_collection(value)
        elif isinstance(value, (int, float)):
            self._log_number(value)
        else:
            self._log_default(value)
        
        self.observer.on_next(value)
    
    def _log_dict(self, value: dict):
        """Log dictionary with pretty formatting."""
        if len(value) <= 3:
            items = ", ".join(f"<blue>{k}</blue>: {v}" for k, v in value.items())
            msg = f"<yellow>[{self.name}]</yellow> Dict: {{{items}}}"
        else:
            msg = f"<yellow>[{self.name}]</yellow> Dict ({len(value)} items):\n"
            for k, v in list(value.items())[:5]:
                msg += f"  - <blue>{k}</blue>: {v}\n"
            if len(value) > 5:
                msg += f"  ... and {len(value) - 5} more items"
        
        logger.opt(raw=True, colors=self.colorize).info(msg)
    
    def _log_collection(self, value: Union[list, tuple]):
        """Log collection with formatting."""
        type_name = type(value).__name__.capitalize()
        items = ", ".join(str(item) for item in value[:5])
        if len(value) > 5:
            items += f"... ({len(value)} total)"
        
        logger.opt(colors=self.colorize).info(
            f"<yellow>[{self.name}]</yellow> {type_name}: <magenta>[{items}]</magenta>"
        )
    
    def _log_number(self, value: Union[int, float]):
        """Log number with color based on value."""
        color = "green" if value > 0 else "red" if value < 0 else "blue"
        type_info = f" <dim>({type(value).__name__})</dim>" if self.show_type else ""
        logger.opt(colors=self.colorize).info(
            f"<yellow>[{self.name}]</yellow> Number: <{color}>{value}</{color}>{type_info}"
        )
    
    def _log_default(self, value: Any):
        """Log any other value type."""
        type_info = f" <dim>({type(value).__name__})</dim>" if self.show_type else ""
        logger.opt(colors=self.colorize).info(
            f"<yellow>[{self.name}]</yellow> Value: {value}{type_info}"
        )
    
    def on_error(self, error):
        """Log error with rich formatting."""
        logger.opt(colors=self.colorize).error(
            f"<yellow>[{self.name}]</yellow> <red>ERROR: {type(error).__name__}: {error}</red>"
        )
        self.observer.on_error(error)
    
    def on_completed(self):
        """Log completion with summary."""
        logger.opt(colors=self.colorize).success(
            f"<yellow>[{self.name}]</yellow> <green>COMPLETED</green> after {self.count} items"
        )
        self.observer.on_completed()


class PerformanceLogger(StatefulOperator[T, T]):
    """Logs performance metrics for reactive streams using Loguru."""
    
    def __init__(self, name: str, log_interval: Optional[int] = None):
        """Initialize performance logger.
        
        Args:
            name: Name for this logger instance
            log_interval: If set, log stats every N items (None = only at completion)
        """
        super().__init__()
        self.name = name
        self.log_interval = log_interval
        self.start_time = None
        self.last_time = None
        self.item_times: List[float] = []
        self.count = 0
        self.log = logger.bind(component="performance", name=name)
    
    def reset_state(self) -> None:
        """Reset timing state."""
        self.start_time = None
        self.last_time = None
        self.item_times = []
        self.count = 0
    
    def on_next(self, value):
        """Track timing and forward value."""
        now = time.time()
        
        # Initialize timing on first item
        if self.start_time is None:
            self.start_time = now
            self.last_time = now
        else:
            # Calculate inter-arrival time
            interval = now - self.last_time
            self.item_times.append(interval)
            self.last_time = now
        
        self.count += 1
        
        # Log stats at intervals if configured
        if self.log_interval and self.count % self.log_interval == 0:
            self._log_stats("PROGRESS")
        
        self.observer.on_next(value)
    
    def on_error(self, error):
        """Log final stats and forward error."""
        self._log_stats("ERROR")
        self.observer.on_error(error)
    
    def on_completed(self):
        """Log final stats and forward completion."""
        self._log_stats("COMPLETED")
        self.observer.on_completed()
    
    def _log_stats(self, status: str = "PROGRESS"):
        """Log performance statistics."""
        if not self.start_time or self.count == 0:
            return
        
        total_time = time.time() - self.start_time
        
        # Calculate metrics
        if self.item_times:
            avg_interval = sum(self.item_times) / len(self.item_times)
            min_interval = min(self.item_times)
            max_interval = max(self.item_times)
            
            # Convert to milliseconds
            avg_ms = avg_interval * 1000
            min_ms = min_interval * 1000
            max_ms = max_interval * 1000
        else:
            avg_ms = min_ms = max_ms = 0
        
        events_per_sec = self.count / total_time if total_time > 0 else 0
        
        # Log performance stats
        self.log.bind(
            status=status,
            events=self.count,
            total_time_sec=round(total_time, 3),
            events_per_sec=round(events_per_sec, 1),
            avg_interval_ms=round(avg_ms, 2),
            min_interval_ms=round(min_ms, 2),
            max_interval_ms=round(max_ms, 2)
        ).info(
            f"PERF [{status}]: {self.count} events in {total_time:.3f}s "
            f"({events_per_sec:.1f}/sec) | "
            f"interval: avg={avg_ms:.2f}ms, min={min_ms:.2f}ms, max={max_ms:.2f}ms"
        )


class ConditionalLogger(BaseOperator[T, T]):
    """Logs only events that meet specified conditions using Loguru."""
    
    def __init__(self,
                 name: str,
                 value_predicate: Optional[Callable[[Any], bool]] = None,
                 error_predicate: Optional[Callable[[Exception], bool]] = None,
                 log_level: str = "INFO",
                 summarize: bool = True):
        """Initialize with filtering predicates.
        
        Args:
            name: Name for this logger
            value_predicate: Function that determines if a value should be logged
            error_predicate: Function that determines if an error should be logged
            log_level: Loguru log level to use
            summarize: Whether to summarize statistics on completion
        """
        super().__init__()
        self.name = name
        self.value_predicate = value_predicate
        self.error_predicate = error_predicate
        self.log_level = log_level.lower()
        self.summarize = summarize
        self.total_count = 0
        self.logged_count = 0
        self.log = logger.bind(operator=name, mode="conditional")
    
    def on_next(self, value):
        """Conditionally log and forward value."""
        self.total_count += 1
        
        should_log = self.value_predicate is None or self.value_predicate(value)
        
        if should_log:
            self.logged_count += 1
            ratio = self.logged_count / self.total_count
            
            log_func = getattr(self.log, self.log_level)
            log_func(
                f"Value: {value} "
                f"(logged {self.logged_count}/{self.total_count}, {ratio:.1%})"
            )
        
        self.observer.on_next(value)
    
    def on_error(self, error):
        """Conditionally log and forward error."""
        should_log = self.error_predicate is None or self.error_predicate(error)
        
        if should_log:
            self.log.error(f"Error: {type(error).__name__}: {error}")
        
        self.observer.on_error(error)
    
    def on_completed(self):
        """Log summary and forward completion."""
        if self.summarize and self.total_count > 0:
            ratio = self.logged_count / self.total_count
            self.log.info(
                f"Completed. Logged {self.logged_count}/{self.total_count} "
                f"values ({ratio:.1%})"
            )
        
        self.observer.on_completed()


# Factory functions for easy operator creation
def log(prefix: str = "RxLog", **kwargs) -> LoggingOperator:
    """Create a basic logging operator."""
    return LoggingOperator(prefix=prefix, **kwargs)


def marble_log(name: str, width: int = 40) -> MarbleLogger:
    """Create a marble diagram logger."""
    return MarbleLogger(name, width)


def context_log(name: str, **context) -> ContextualLogger:
    """Create a contextual logger with the given name and context values."""
    return ContextualLogger(name, context)


def rich_log(name: str, **kwargs) -> RichLoggerOperator:
    """Create a rich formatting logger."""
    return RichLoggerOperator(name, **kwargs)


def perf_log(name: str, log_interval: Optional[int] = None) -> PerformanceLogger:
    """Create a performance monitoring logger."""
    return PerformanceLogger(name, log_interval)


def conditional_log(name: str, **kwargs) -> ConditionalLogger:
    """Create a conditional logger."""
    return ConditionalLogger(name, **kwargs)


# Helper functions for quick debugging
def debug_stream(name: str = "Debug") -> Callable:
    """Add comprehensive debugging to an observable using Loguru.
    
    Usage:
        source.pipe(
            debug_stream("Before"),
            ops.map(transform),
            debug_stream("After")
        )
    """
    debug_logger = logger.bind(operator=name)
    
    return ops.do_action(
        on_next=lambda x: debug_logger.debug(f"Next: {x!r}"),
        on_error=lambda e: debug_logger.error(f"Error: {type(e).__name__}: {e}"),
        on_completed=lambda: debug_logger.info("Completed")
    )


def timestamp_stream(name: str = "Timestamp") -> Callable:
    """Add timestamping to an observable using Loguru.
    
    Usage:
        source.pipe(
            timestamp_stream("Start"),
            # ... operations ...
            timestamp_stream("End")
        )
    """
    start_time = time.time()
    ts_logger = logger.bind(operator=name)
    
    def format_time():
        elapsed = time.time() - start_time
        return f"{elapsed:.3f}s"
    
    return ops.do_action(
        on_next=lambda x: ts_logger.info(f"[{format_time()}] Next: {type(x).__name__}"),
        on_error=lambda e: ts_logger.error(f"[{format_time()}] Error: {type(e).__name__}"),
        on_completed=lambda: ts_logger.success(f"[{format_time()}] Completed")
    )