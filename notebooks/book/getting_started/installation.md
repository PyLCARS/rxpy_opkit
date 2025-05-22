# Installation

## Prerequisites

RxPy OpKit requires Python 3.10 or higher.

## Installation from Source

To install RxPy OpKit from source:

```bash
# Clone the repository
git clone https://github.com/GProtoZeroW/rxpy_opkit.git
cd rxpy_opkit

# Create a virtual environment using pyenv (recommended)
pyenv virtualenv 3.13.1 rxpy_opkit
pyenv local rxpy_opkit

# Install in development mode
pip install -e .
```

## Dependencies

RxPy OpKit depends on the following packages:

- `reactivex`: The core reactive programming library
- `loguru`: For logging functionality
- `attrs`: For class definitions (preferred over dataclasses)

These dependencies will be automatically installed when you install RxPy OpKit.
