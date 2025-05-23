"""Logging operators module for RxPy OpKit.

This module provides various operators for logging, debugging, and monitoring
reactive streams using Loguru for rich, structured logging.
"""

from .logging_operators import (
    # Operator classes
    LoggingOperator,
    MarbleLogger,
    ContextualLogger,
    RichLoggerOperator,
    PerformanceLogger,
    ConditionalLogger,
    
    # Factory functions
    log,
    marble_log,
    context_log,
    rich_log,
    perf_log,
    conditional_log,
    
    # Helper functions
    debug_stream,
    timestamp_stream,
)

__all__ = [
    # Operators
    "LoggingOperator",
    "MarbleLogger", 
    "ContextualLogger",
    "RichLoggerOperator",
    "PerformanceLogger",
    "ConditionalLogger",
    
    # Factory functions
    "log",
    "marble_log",
    "context_log",
    "rich_log",
    "perf_log",
    "conditional_log",
    
    # Helpers
    "debug_stream",
    "timestamp_stream",
]

__version__ = "0.1.0"