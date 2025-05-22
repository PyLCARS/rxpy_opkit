"""RxPy OpKit - Extended operators for RxPy.

A collection of custom operators for RxPy including:
- Foundation classes for building custom operators
- Logging and debugging operators
- Missing operators from other Rx implementations
"""

# Import and re-export from sub-modules
from .basis import (
    BaseOperator,
    StatefulOperator,
    CompositeOperator,
    SimpleOperator,
    FilteringOperator,
    create_operator,
)

from .logging_ops import (
    LoggingOperator,
    MarbleLogger,
    ContextualLogger,
    RichLoggerOperator,
    PerformanceLogger,
    ConditionalLogger,
    log,
    marble_log,
    context_log,
    rich_log,
    perf_log,
    conditional_log,
    debug_stream,
    timestamp_stream,
)

__all__ = [
    # Basis classes
    "BaseOperator",
    "StatefulOperator",
    "CompositeOperator",
    "SimpleOperator",
    "FilteringOperator",
    "create_operator",
    
    # Logging operators
    "LoggingOperator",
    "MarbleLogger",
    "ContextualLogger",
    "RichLoggerOperator",
    "PerformanceLogger",
    "ConditionalLogger",
    
    # Logging factory functions
    "log",
    "marble_log",
    "context_log",
    "rich_log",
    "perf_log",
    "conditional_log",
    
    # Logging helpers
    "debug_stream",
    "timestamp_stream",
]

__version__ = "0.1.0"
__author__ = "GProtoZeroW"
__email__ = "11997114+GProtoZeroW@users.noreply.github.com"