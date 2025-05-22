# %% [markdown]
# # Simple RxPy Operators Example
# 
# This notebook demonstrates basic usage of custom operators from rxpy_opkit.

# %% [markdown]
# ## Imports

# %%
import reactivex as rx
from reactivex import operators as ops
from loguru import logger

# This will be where our custom operators are imported
# from rxpy_opkit.operators import custom_op1, custom_op2

# %% [markdown]
# ## Basic RxPy Stream

# %%
# Create a simple observable
source = rx.of(1, 2, 3, 4, 5)

# Apply standard operators
result = source.pipe(
    ops.map(lambda x: x * 10),
    ops.filter(lambda x: x > 20)
)

# Subscribe and print the results
result.subscribe(
    on_next=lambda x: logger.info(f"Received: {x}"),
    on_error=lambda e: logger.error(f"Error: {e}"),
    on_completed=lambda: logger.info("Completed")
)

# %% [markdown]
# ## Using Custom Operators
# 
# Once custom operators are implemented, they can be used like this:

# %%
# Example of future custom operator usage
# source.pipe(
#     custom_op1(),
#     custom_op2(param="value")
# ).subscribe(
#     on_next=lambda x: logger.info(f"Custom op result: {x}"),
#     on_completed=lambda: logger.info("Custom processing completed")
# )
