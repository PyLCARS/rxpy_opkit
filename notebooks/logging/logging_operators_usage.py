# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: title,-all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.17.0
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# # RxPy OpKit: Logging Operators Guide
#
# This notebook demonstrates all the logging operators available in RxPy OpKit. These operators help you debug, monitor, and understand the behavior of your reactive streams.

# %% [markdown]
# # Setup and Imports

# %%
# Add project root and src to Python path
import sys
import os
from pathlib import Path

# Directly use the absolute path to the project root
# This works both in notebooks and in scripts
project_root = Path('/media/storage/GShared/Todays_Projects/rxpy_opkit')
src_dir = project_root / 'src'

# Print diagnostic information
print(f"Project root: {project_root}")
print(f"Source directory: {src_dir}")
print(f"Directory exists: {project_root.exists()}")
print(f"Source exists: {src_dir.exists()}")

# In case the hard-coded path doesn't work, try to find the project root
if not src_dir.exists():
    print("Hard-coded path didn't work, trying to find project root...")
    try:
        # When running as a script
        script_path = Path(__file__).resolve()
        project_root = script_path.parent.parent.parent
        src_dir = project_root / 'src'
        print(f"Script-based project root: {project_root}")
    except NameError:
        # When in Jupyter, try working up from current directory
        cwd = Path.cwd()
        print(f"Current working directory: {cwd}")
        
        # If we're in notebooks/logging, go up two directories
        if cwd.name == 'logging' and cwd.parent.name == 'notebooks':
            project_root = cwd.parent.parent
        # If we're in notebooks, go up one directory
        elif cwd.name == 'notebooks':
            project_root = cwd.parent
        # Otherwise assume we're at the project root
        else:
            project_root = cwd
            
        src_dir = project_root / 'src'
        print(f"Notebook-based project root: {project_root}")


# Add both project root and src to Python path if not already there
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Verify the package can be imported
try:
    import rxpy_opkit
    print(f"Successfully imported rxpy_opkit from: {rxpy_opkit.__file__}")
except ImportError as e:
    print(f"Failed to import rxpy_opkit: {e}")
    print(f"Python path: {sys.path}")
    raise

import reactivex as rx
from reactivex import operators as ops
import time
import random
from loguru import logger

# Import logging operators from rxpy_opkit
from rxpy_opkit.logging_ops import (
    log, marble_log, context_log, rich_log, perf_log, conditional_log,
    debug_stream, timestamp_stream
)

# %% [markdown]
# # Logging (Loguru) Setup

# %%
# Configure loguru for notebook output
logger.remove()
logger.add(
    sys.stdout,
    format="<green>{time:HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan> - <level>{message}</level>",
    colorize=True,
    level="INFO"
)

# %% [markdown]
# # Logging Operators from `rxpy-opkit`

# %% [markdown]
# ## `log` - Basic Logging Operator

# %% [markdown]
# ### Description and Behavior
#
# The `log` operator is the simplest logging operator that logs all events passing through a stream. It's perfect for basic debugging and understanding data flow.
#
# **Behavior Details:**
# - **On Next**: Logs each value with a counter and optional custom formatting
# - **On Complete**: Logs completion with total count of values processed
# - **On Error**: Logs error type and message
# - **Internal Errors**: Formatting errors are caught and logged without interrupting the stream

# %% Styling [markdown]
# ```mermaid
# flowchart TD
#     subgraph "Source Observable"
#         SNext["on_next: value"]
#         SComplete["on_completed"]
#         SError["on_error: err"]
#     end
#     
#     subgraph "log Operator"
#         LogValue["Log value with<br/>prefix and count"]
#         LogError["Log error type<br/>and message"]
#         LogComplete["Log completion<br/>with total count"]
#         FormatValue["Format value<br/>(truncate if needed)"]
#     end
#     
#     subgraph "Subscriber"
#         ONext["on_next: value<br/>(unchanged)"]
#         OComplete["on_completed"]
#         OError["on_error: err"]
#     end
#     
#
#     SNext --> FormatValue
#     FormatValue --> LogValue
#     LogValue --> ONext
#     
#
#     SComplete --> LogComplete
#     LogComplete --> OComplete
#     
#
#     SError --> LogError
#     LogError --> OError
#     
#
#     style SNext fill:#e4f7fb,stroke:#333
#     style SComplete fill:#e4f7fb,stroke:#333
#     style SError fill:#e4f7fb,stroke:#333
#     
#     style LogValue fill:#f96,stroke:#333
#     style LogError fill:#f96,stroke:#333
#     style LogComplete fill:#f96,stroke:#333
#     style FormatValue fill:#f96,stroke:#333
#     
#     style ONext fill:#d5f5d5,stroke:#333
#     style OComplete fill:#d5f5d5,stroke:#333
#     style OError fill:#ffcccc,stroke:#333
# ```

# %% [markdown]
# ### When to Use/Avoid and Alternatives

# %% [markdown]
# **When to Use:**
# - Quick debugging of data flow through operators
# - Understanding what values are being emitted
# - Counting items in a stream
# - Basic stream monitoring in development

# %% [markdown]
# **When to Avoid:**
# - Production environments (unless with appropriate log levels)
# - High-frequency streams (can flood logs)
# - When you need structured logging (use `context_log` instead)

# %% [markdown]
# **Alternatives:**
# - `do_action`: Use built-in `do_action` with custom lambda for simple logging
# - `context_log`: For structured logging with additional context
# - `conditional_log`: To reduce log volume by filtering what gets logged

# %% [markdown]
# ### Nominal Usage Examples

# %% [markdown]
# #### Basic Example

# %%
# Basic example demonstrating log operator
source = rx.of(1, 2, 3, 4, 5)

# Add logging at different points in the pipeline
result = source.pipe(
    log("Input"),
    ops.map(lambda x: x * 10),
    log("Mapped"),
    ops.filter(lambda x: x > 25),
    log("Filtered")
)

print("Example: Basic log operator")
print("---------------------------")
result.subscribe(
    on_next=lambda i: print(f"Final result: {i}"),
    on_completed=lambda: print("Stream completed")
)

# %% [markdown]
# ```mermaid
# sequenceDiagram
#     participant Source
#     participant Log1 as log("Input")
#     participant Map as map(x*10)
#     participant Log2 as log("Mapped")
#     participant Filter as filter(>25)
#     participant Log3 as log("Filtered")
#     participant Observer
#     
#     Source->>Log1: 1
#     Note over Log1: [Input] [1] Value: 1
#     Log1->>Map: 1
#     Map->>Log2: 10
#     Note over Log2: [Mapped] [1] Value: 10
#     Log2->>Filter: 10
#     Note over Filter: 10 <= 25, filtered out
#     
#     Source->>Log1: 2
#     Note over Log1: [Input] [2] Value: 2
#     Log1->>Map: 2
#     Map->>Log2: 20
#     Note over Log2: [Mapped] [2] Value: 20
#     Log2->>Filter: 20
#     Note over Filter: 20 <= 25, filtered out
#     
#     Source->>Log1: 3
#     Note over Log1: [Input] [3] Value: 3
#     Log1->>Map: 3
#     Map->>Log2: 30
#     Note over Log2: [Mapped] [3] Value: 30
#     Log2->>Filter: 30
#     Filter->>Log3: 30
#     Note over Log3: [Filtered] [1] Value: 30
#     Log3->>Observer: 30
#     
#     Source->>Log1: complete
#     Note over Log1: [Input] Completed after 5 values
#     Log1->>Map: complete
#     Map->>Log2: complete
#     Note over Log2: [Mapped] Completed after 5 values
#     Log2->>Filter: complete
#     Filter->>Log3: complete
#     Note over Log3: [Filtered] Completed after 3 values
#     Log3->>Observer: complete
# ```

# %% [markdown]
# #### Custom Formatting Example

# %%
# Custom formatter for complex objects
def custom_formatter(value):
    if isinstance(value, dict):
        return f"User(id={value.get('id')}, name={value.get('name')})"
    return str(value)

# Source with dictionary values
users = rx.of(
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
)

result = users.pipe(
    log("Users", value_formatter=custom_formatter),
    ops.map(lambda u: u["name"].upper()),
    log("Names")
)

print("\nExample: Custom Value Formatting")
print("--------------------------------")
result.subscribe()

# %% [markdown]
# ### Error Handling

# %% [markdown]
# Common errors when using `log` operator:
# 1. **Formatter errors**: Custom formatters may fail on unexpected value types
# 2. **String conversion errors**: Some objects may not have proper string representations
# 3. **Performance impact**: Logging every value in high-frequency streams
#
# **Best Practices:**
# - Use safe formatters that handle exceptions
# - Configure appropriate log levels for different environments
# - Consider `conditional_log` for high-frequency streams

# %% [markdown]
# #### Example: Handling Formatter Errors

# %%
# Formatter that might fail
def risky_formatter(value):
    # This will fail if value doesn't have 'data' attribute
    return f"Data: {value.data}"

# Mix of values, some will cause formatter errors
source = rx.of(
    {"data": "good"},
    "bad_value",  # This will cause formatter error
    {"data": "also_good"}
)

result = source.pipe(
    log("Risky", value_formatter=risky_formatter)
)

print("\nExample: Formatter Error Handling")
print("---------------------------------")
result.subscribe(
    on_next=lambda x: print(f"Received: {x}"),
    on_error=lambda e: print(f"Stream error: {e}")
)

# %% [markdown]
# ## `marble_log` - ASCII Marble Diagram Logger

# %% [markdown]
# ### Description and Behavior
#
# The `marble_log` operator creates ASCII marble diagrams to visualize the timing and sequence of events in a stream. It's excellent for understanding async behavior and timing.
#
# **Behavior Details:**
# - **On Next**: Adds a symbol to the timeline representing the value
# - **On Complete**: Shows completion marker `|` on the timeline
# - **On Error**: Shows error marker `X` on the timeline
# - **Internal Errors**: None expected (simple string operations)

# %% Styling [markdown]
# ```mermaid
# flowchart TD
#     subgraph "Source Observable"
#         SNext["on_next: value"]
#         SComplete["on_completed"]
#         SError["on_error: err"]
#     end
#     
#     subgraph "marble_log Operator"
#         AddToTimeline["Add event to timeline"]
#         SelectSymbol["Select symbol:<br/>• numbers: first digit<br/>• strings: first char<br/>• other: •"]
#         PrintTimeline["Print timeline with<br/>dashes and symbols"]
#         MarkComplete["Add | symbol"]
#         MarkError["Add X symbol"]
#     end
#     
#     subgraph "Subscriber"
#         ONext["on_next: value<br/>(unchanged)"]
#         OComplete["on_completed"]
#         OError["on_error: err"]
#     end
#     
#
#     SNext --> SelectSymbol
#     SelectSymbol --> AddToTimeline
#     AddToTimeline --> PrintTimeline
#     PrintTimeline --> ONext
#     
#
#     SComplete --> MarkComplete
#     MarkComplete --> PrintTimeline
#     PrintTimeline --> OComplete
#     
#
#     SError --> MarkError
#     MarkError --> PrintTimeline
#     PrintTimeline --> OError
#     
#
#     style SNext fill:#e4f7fb,stroke:#333
#     style SComplete fill:#e4f7fb,stroke:#333
#     style SError fill:#e4f7fb,stroke:#333
#     
#     style AddToTimeline fill:#f96,stroke:#333
#     style SelectSymbol fill:#f96,stroke:#333
#     style PrintTimeline fill:#f96,stroke:#333
#     style MarkComplete fill:#f96,stroke:#333
#     style MarkError fill:#f96,stroke:#333
#     
#     style ONext fill:#d5f5d5,stroke:#333
#     style OComplete fill:#d5f5d5,stroke:#333
#     style OError fill:#ffcccc,stroke:#333
# ```

# %% [markdown]
# ### When to Use/Avoid and Alternatives

# %% [markdown]
# **When to Use:**
# - Visualizing timing of async operations
# - Understanding operator behavior with delays
# - Teaching/demonstrating reactive concepts
# - Debugging race conditions or timing issues

# %% [markdown]
# **When to Avoid:**
# - Production code (it's a debugging tool)
# - Very long-running streams (timeline gets truncated)
# - When you need precise timing measurements (use `perf_log`)

# %% [markdown]
# **Alternatives:**
# - `timestamp`: Built-in operator to add timestamps to values
# - `perf_log`: For precise performance measurements
# - External visualization tools for production monitoring

# %% [markdown]
# ### Nominal Usage Examples

# %% [markdown]
# #### Basic Marble Diagram

# %%
# Create an interval observable for timing visualization
source = rx.interval(0.2).pipe(
    ops.take(10),
    marble_log("Source", width=30),
    ops.map(lambda x: x * 2),
    marble_log("Mapped", width=30),
    ops.filter(lambda x: x % 4 == 0),
    marble_log("Filtered", width=30)
)

print("Example: Marble Diagram Visualization")
print("------------------------------------")
# This will show the marble diagram in real-time
subscription = source.subscribe()
time.sleep(2.5)  # Let it run
subscription.dispose()

# %% [markdown]
# #### Multiple Streams Comparison

# %%
# Compare two different streams
stream1 = rx.interval(0.3).pipe(
    ops.take(5),
    ops.map(lambda x: f"A{x}"),
    marble_log("Stream A", width=40)
)

stream2 = rx.interval(0.2).pipe(
    ops.take(7),
    ops.map(lambda x: f"B{x}"),
    marble_log("Stream B", width=40)
)

merged = rx.merge(stream1, stream2).pipe(
    marble_log("Merged", width=40)
)

print("\nExample: Multiple Stream Comparison")
print("-----------------------------------")
sub = merged.subscribe()
time.sleep(1.8)
sub.dispose()

# %% [markdown]
# ## `context_log` - Contextual Logger with Structured Data

# %% [markdown]
# ### Description and Behavior
#
# The `context_log` operator adds rich contextual information to every log entry, including timing, event counts, and custom context fields. Perfect for structured logging and production monitoring.
#
# **Behavior Details:**
# - **On Next**: Logs with event count, elapsed time, value type, and custom context
# - **On Complete**: Logs with final statistics and elapsed time
# - **On Error**: Logs with error details and context
# - **Internal Errors**: None expected (robust error handling)

# %% Styling [markdown]
# ```mermaid
# flowchart TD
#     subgraph "Source Observable"
#         SNext["on_next: value"]
#         SComplete["on_completed"]
#         SError["on_error: err"]
#     end
#     
#     subgraph "context_log Operator"
#         BindContext["Bind logger with<br/>operator name & context"]
#         CalcElapsed["Calculate elapsed time<br/>since start"]
#         IncrementCount["Increment event counter"]
#         LogWithContext["Log with:<br/>• event type<br/>• count<br/>• elapsed time<br/>• value type<br/>• custom context"]
#     end
#     
#     subgraph "Subscriber"
#         ONext["on_next: value<br/>(unchanged)"]
#         OComplete["on_completed"]
#         OError["on_error: err"]
#     end
#     
#
#     SNext --> IncrementCount
#     IncrementCount --> CalcElapsed
#     CalcElapsed --> LogWithContext
#     LogWithContext --> ONext
#     
#
#     SComplete --> CalcElapsed
#     CalcElapsed --> LogWithContext
#     LogWithContext --> OComplete
#     
#
#     SError --> CalcElapsed
#     CalcElapsed --> LogWithContext
#     LogWithContext --> OError
#     
#
#     style SNext fill:#e4f7fb,stroke:#333
#     style SComplete fill:#e4f7fb,stroke:#333
#     style SError fill:#e4f7fb,stroke:#333
#     
#     style BindContext fill:#f96,stroke:#333
#     style CalcElapsed fill:#f96,stroke:#333
#     style IncrementCount fill:#f96,stroke:#333
#     style LogWithContext fill:#f96,stroke:#333
#     
#     style ONext fill:#d5f5d5,stroke:#333
#     style OComplete fill:#d5f5d5,stroke:#333
#     style OError fill:#ffcccc,stroke:#333
# ```

# %% [markdown]
# ### When to Use/Avoid and Alternatives

# %% [markdown]
# **When to Use:**
# - Production logging with structured data
# - Tracking request/response flows with correlation IDs
# - Performance monitoring with business context
# - Debugging complex multi-step processes

# %% [markdown]
# **When to Avoid:**
# - Simple debugging (use `log` instead)
# - When you don't need structured data
# - High-frequency streams without sampling

# %% [markdown]
# **Alternatives:**
# - `log`: For simple debugging without structure
# - Custom `do_action`: For specific logging requirements
# - External APM tools for production monitoring

# %% [markdown]
# ### Nominal Usage Examples

# %% [markdown]
# #### API Request Processing

# %%
# Simulate API request processing with context
def process_request(request_id):
    return rx.of(
        {"step": "validate", "status": "ok"},
        {"step": "authorize", "status": "ok"},
        {"step": "process", "status": "ok"},
        {"step": "respond", "status": "ok"}
    ).pipe(
        ops.delay(0.1),
        context_log("RequestProcessor", 
                   request_id=request_id,
                   user_id="user123",
                   endpoint="/api/orders")
    )

print("Example: API Request Context Logging")
print("-----------------------------------")
process_request("req-12345").subscribe()
time.sleep(0.5)

# %% [markdown]
# #### Multi-Service Pipeline

# %%
# Simulate multi-service data pipeline
order_data = {
    "order_id": "ORD-789",
    "customer_id": "CUST-456",
    "total": 150.00,
    "items": ["item1", "item2", "item3"]
}

pipeline = rx.of(order_data).pipe(
    context_log("OrderService", service="order", environment="prod"),
    ops.map(lambda order: {**order, "validated": True}),
    context_log("ValidationService", service="validation", environment="prod"),
    ops.map(lambda order: {**order, "payment_id": "PAY-" + order["order_id"]}),
    context_log("PaymentService", service="payment", environment="prod")
)

print("\nExample: Multi-Service Pipeline")
print("-------------------------------")
pipeline.subscribe()

# %% [markdown]
# ## `rich_log` - Rich Formatting Logger

# %% [markdown]
# ### Description and Behavior
#
# The `rich_log` operator provides enhanced formatting for different data types with color coding and special formatting for collections, numbers, and complex objects.
#
# **Behavior Details:**
# - **On Next**: Formats values based on type with colors and structure
# - **On Complete**: Shows completion with item count in green
# - **On Error**: Shows errors in red with highlighting
# - **Internal Errors**: Gracefully handles formatting failures

# %% [markdown]
# ### Nominal Usage Examples

# %%
# Example with various data types
mixed_data = rx.of(
    42,
    -15,
    0,
    {"name": "Alice", "age": 30, "city": "NYC"},
    ["apple", "banana", "cherry", "date", "elderberry", "fig"],
    "Simple string",
    3.14159,
    {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5, "f": 6}
)

result = mixed_data.pipe(
    rich_log("DataStream", colorize=True, show_type=True)
)

print("Example: Rich Formatted Logging")
print("-------------------------------")
result.subscribe()

# %% [markdown]
# ## `perf_log` - Performance Monitoring Logger

# %% [markdown]
# ### Description and Behavior
#
# The `perf_log` operator tracks and logs performance metrics including timing, throughput, and interval statistics. Essential for performance optimization.
#
# **Behavior Details:**
# - **On Next**: Tracks inter-arrival times and counts events
# - **On Complete**: Logs comprehensive performance statistics
# - **On Error**: Logs statistics up to the error point
# - **Internal Errors**: None expected (simple arithmetic)

# %% Styling [markdown]
# ```mermaid
# flowchart TD
#     subgraph "Source Observable"
#         SNext["on_next: value"]
#         SComplete["on_completed"]
#         SError["on_error: err"]
#     end
#     
#     subgraph "perf_log Operator"
#         RecordTime["Record current time"]
#         CalcInterval["Calculate interval<br/>since last event"]
#         StoreInterval["Store interval in list"]
#         CheckLogInterval["Log interval<br/>reached?"]
#         CalcStats["Calculate:<br/>• avg/min/max interval<br/>• events per second<br/>• total time"]
#         LogStats["Log performance stats"]
#     end
#     
#     subgraph "Subscriber"
#         ONext["on_next: value<br/>(unchanged)"]
#         OComplete["on_completed"]
#         OError["on_error: err"]
#     end
#     
#
#     SNext --> RecordTime
#     RecordTime --> CalcInterval
#     CalcInterval --> StoreInterval
#     StoreInterval --> CheckLogInterval
#     CheckLogInterval -->|Yes| CalcStats
#     CheckLogInterval -->|No| ONext
#     CalcStats --> LogStats
#     LogStats --> ONext
#     
#
#     SComplete --> CalcStats
#     CalcStats --> LogStats
#     LogStats --> OComplete
#     
#
#     SError --> CalcStats
#     CalcStats --> LogStats
#     LogStats --> OError
#     
#
#     style SNext fill:#e4f7fb,stroke:#333
#     style SComplete fill:#e4f7fb,stroke:#333
#     style SError fill:#e4f7fb,stroke:#333
#     
#     style RecordTime fill:#f96,stroke:#333
#     style CalcInterval fill:#f96,stroke:#333
#     style StoreInterval fill:#f96,stroke:#333
#     style CheckLogInterval fill:#f96,stroke:#333
#     style CalcStats fill:#f96,stroke:#333
#     style LogStats fill:#f96,stroke:#333
#     
#     style ONext fill:#d5f5d5,stroke:#333
#     style OComplete fill:#d5f5d5,stroke:#333
#     style OError fill:#ffcccc,stroke:#333
# ```

# %% [markdown]
# ### When to Use/Avoid and Alternatives

# %% [markdown]
# **When to Use:**
# - Identifying performance bottlenecks
# - Monitoring production stream throughput
# - Comparing operator performance
# - Capacity planning and optimization

# %% [markdown]
# **When to Avoid:**
# - Very short streams (statistics not meaningful)
# - When timing precision isn't important
# - Development/debugging (use simpler loggers)

# %% [markdown]
# **Alternatives:**
# - `scan` with custom timing logic
# - External monitoring tools (Prometheus, etc.)
# - Built-in `timestamp` operator for raw timestamps

# %% [markdown]
# ### Nominal Usage Examples

# %% [markdown]
# #### Performance Comparison

# %%
# Compare performance of different operators
def heavy_computation(x):
    # Simulate varying computation time
    time.sleep(random.uniform(0.01, 0.05))
    return x ** 2

# Source with consistent interval
source = rx.interval(0.1).pipe(ops.take(20))

# Pipeline with performance monitoring
pipeline = source.pipe(
    perf_log("Source", log_interval=10),
    ops.map(heavy_computation),
    perf_log("After Heavy Computation", log_interval=10),
    ops.filter(lambda x: x % 2 == 0),
    perf_log("After Filter", log_interval=10)
)

print("Example: Performance Monitoring")
print("------------------------------")
sub = pipeline.subscribe()
time.sleep(2.5)
sub.dispose()

# %% [markdown]
# #### Batch Processing Performance

# %%
# Monitor batch processing performance
batches = rx.interval(0.5).pipe(
    ops.take(5),
    ops.map(lambda i: list(range(i * 10, (i + 1) * 10))),
    perf_log("Batch Generator"),
    ops.flat_map(lambda batch: rx.from_(batch)),
    ops.scan(lambda acc, x: acc + x, 0),
    perf_log("Accumulator", log_interval=20)
)

print("\nExample: Batch Processing Performance")
print("------------------------------------")
sub = batches.subscribe(on_next=lambda x: None)  # Suppress output
time.sleep(3)
sub.dispose()

# %% [markdown]
# ## `conditional_log` - Filtered Logging Operator

# %% [markdown]
# ### Description and Behavior
#
# The `conditional_log` operator only logs events that meet specified criteria, reducing log volume while maintaining visibility into important events.
#
# **Behavior Details:**
# - **On Next**: Logs only if value predicate returns True
# - **On Complete**: Logs summary of logged vs total events
# - **On Error**: Logs only if error predicate returns True
# - **Internal Errors**: Predicate exceptions are handled gracefully

# %% [markdown]
# ### Nominal Usage Examples

# %% [markdown]
# #### Log Only Errors and Warnings

# %%
# Stream with mixed success/error responses
responses = rx.from_([
    {"status": 200, "data": "ok"},
    {"status": 404, "error": "not found"},
    {"status": 200, "data": "ok"},
    {"status": 500, "error": "server error"},
    {"status": 200, "data": "ok"},
    {"status": 403, "error": "forbidden"}
])

# Only log errors
error_responses = responses.pipe(
    conditional_log(
        "ErrorMonitor",
        value_predicate=lambda r: r.get("status", 200) >= 400,
        log_level="WARNING"
    )
)

print("Example: Conditional Error Logging")
print("---------------------------------")
error_responses.subscribe()

# %% [markdown]
# #### High-Value Transaction Logging

# %%
# Stream of transactions
transactions = rx.from_([
    {"id": 1, "amount": 10.50, "type": "purchase"},
    {"id": 2, "amount": 1500.00, "type": "purchase"},
    {"id": 3, "amount": 25.00, "type": "refund"},
    {"id": 4, "amount": 5000.00, "type": "purchase"},
    {"id": 5, "amount": 75.00, "type": "purchase"},
])

# Only log high-value transactions
high_value = transactions.pipe(
    conditional_log(
        "HighValueMonitor",
        value_predicate=lambda t: t["amount"] > 1000,
        summarize=True
    )
)

print("\nExample: High-Value Transaction Monitoring")
print("-----------------------------------------")
high_value.subscribe()

# %% [markdown]
# ## Helper Functions

# %% [markdown]
# ### `debug_stream` - Quick Debugging Helper

# %% [markdown]
# #### Description
#
# A convenience function that uses `do_action` to quickly add debug logging at any point in a pipeline.

# %%
# Quick debugging example
rx.range(1, 5).pipe(
    debug_stream("Input"),
    ops.map(lambda x: x ** 2),
    debug_stream("Squared"),
    ops.filter(lambda x: x > 5),
    debug_stream("Filtered")
).subscribe()

# %% [markdown]
# ### `timestamp_stream` - Timing Helper

# %% [markdown]
# #### Description
#
# Adds elapsed time information to log messages, useful for understanding timing in async operations.

# %%
# Timing analysis example
rx.interval(0.2).pipe(
    ops.take(5),
    timestamp_stream("Start"),
    ops.delay(0.1),
    timestamp_stream("After Delay"),
    ops.scan(lambda acc, x: acc + x, 0),
    timestamp_stream("After Scan")
).subscribe(on_next=lambda x: None)

time.sleep(1.5)

# %% [markdown]
# ## Best Practices and Tips

# %% [markdown]
# ### 1. **Choose the Right Logger**
# - `log`: Basic debugging
# - `marble_log`: Timing visualization
# - `context_log`: Production structured logging
# - `rich_log`: Complex data inspection
# - `perf_log`: Performance analysis
# - `conditional_log`: High-volume stream filtering

# %% [markdown]
# ### 2. **Performance Considerations**
# ```python
# # Bad: Logging everything in high-frequency stream
# rx.interval(0.001).pipe(
#     log("Too Much!")  # Don't do this!
# )
#
# # Good: Sample or filter before logging
# rx.interval(0.001).pipe(
#     ops.sample(1.0),  # Sample once per second
#     log("Sampled")
# )
#
# # Better: Use conditional logging
# rx.interval(0.001).pipe(
#     ops.scan(lambda acc, x: acc + 1, 0),
#     conditional_log("Every100th", 
#                    value_predicate=lambda x: x % 100 == 0)
# )
# ```

# %% [markdown]
# ### 3. **Combining Loggers**
# ```python
# # Use different loggers for different aspects
# stream.pipe(
#     context_log("Service", request_id="123"),  # Structure
#     ops.map(transform),
#     perf_log("Transform", log_interval=100),   # Performance
#     ops.filter(validate),
#     conditional_log("Errors",                   # Errors only
#                    value_predicate=lambda x: x.get("error"))
# )
# ```

# %% [markdown]
# ### 4. **Production vs Development**
# ```python
# # Development: verbose logging
# if DEBUG:
#     pipeline = source.pipe(
#         log("Debug"),
#         marble_log("Timing"),
#         ops.map(process),
#         rich_log("Results")
#     )
# else:
#     # Production: selective logging
#     pipeline = source.pipe(
#         context_log("ProdService", env="prod"),
#         ops.map(process),
#         conditional_log("Warnings", 
#                        value_predicate=lambda x: x.severity > "INFO")
#     )
# ```

# %% [markdown]
# ## Error Handling Examples

# %% [markdown]
# ### Graceful Error Handling in Streams

# %%
# Stream that might have errors
def risky_operation(x):
    if x == 3:
        raise ValueError(f"Cannot process {x}")
    return x * 2

source = rx.from_([1, 2, 3, 4, 5])

# Log errors without stopping the stream
result = source.pipe(
    log("Input"),
    ops.map(lambda x: rx.just(x).pipe(
        ops.map(risky_operation),
        ops.catch(lambda e, src: rx.of(f"ERROR: {e}"))
    )),
    ops.merge_all(),
    log("Output"),
)

print("Example: Error Handling with Logging")
print("-----------------------------------")
result.subscribe()

# %% [markdown]
# ### Performance Impact of Logging

# %%
# Demonstrate performance impact
import timeit

def no_logging():
    rx.range(1000).pipe(
        ops.map(lambda x: x * 2),
        ops.filter(lambda x: x % 2 == 0)
    ).subscribe(on_next=lambda x: None)

def with_logging():
    rx.range(1000).pipe(
        log("Input", log_values=True, log_completion=False),
        ops.map(lambda x: x * 2),
        log("Mapped", log_values=True, log_completion=False),
        ops.filter(lambda x: x % 2 == 0),
        log("Filtered", log_values=True, log_completion=False)
    ).subscribe(on_next=lambda x: None)

# Temporarily suppress logging output for timing
logger.remove()

no_log_time = timeit.timeit(no_logging, number=10)
with_log_time = timeit.timeit(with_logging, number=10)

# Re-enable logging
logger.add(sys.stdout, level="INFO")

print(f"\nPerformance Impact of Logging:")
print(f"Without logging: {no_log_time:.4f}s")
print(f"With logging: {with_log_time:.4f}s")
print(f"Overhead: {((with_log_time - no_log_time) / no_log_time) * 100:.1f}%")

# %% [markdown]
# ## Summary
#
# The RxPy OpKit logging operators provide a comprehensive toolkit for debugging and monitoring reactive streams:
#
# 1. **Basic Logging** (`log`) - Simple, effective debugging
# 2. **Visual Logging** (`marble_log`) - ASCII marble diagrams
# 3. **Structured Logging** (`context_log`) - Production-ready with context
# 4. **Pretty Logging** (`rich_log`) - Enhanced formatting for complex data
# 5. **Performance Logging** (`perf_log`) - Detailed timing analysis
# 6. **Filtered Logging** (`conditional_log`) - Reduce log volume intelligently
#
# Choose the right logger for your use case and remember to consider performance impacts in production environments.

# %% [markdown]
# ### Documentation and Reference Links
#
# - [RxPy OpKit GitHub Repository](#) - Source code and examples
# - [RxPy Documentation](https://rxpy.readthedocs.io/) - Official RxPy docs
# - [Loguru Documentation](https://loguru.readthedocs.io/) - Logging library used
# - [Reactive Extensions](http://reactivex.io/) - ReactiveX concepts and patterns
