# RxPy OpKit Notebooks

This directory contains Jupyter notebooks and related documentation for RxPy OpKit.

## Directory Structure

- `book/` - Jupyter Book configuration files
  - `_config.yml` - Book configuration
  - `_toc.yml` - Table of contents (with commented entries for future notebooks)
  - `intro.md` - Introduction page

- `flat_operators/` - Notebooks about flat class-based operators
- `logging/` - Notebooks about logging operators
- `missing_operators/` - Notebooks about operators missing from RxPy
- `testing/` - Notebooks about testing reactive code

## Creating Notebooks

When creating new notebooks, follow these conventions:

1. Use jupytext with the percent format (`# %%`) for cell markers
2. Add proper markdown cells with explanations
3. Include executable examples
4. Include output cells when appropriate

## Building the Documentation

Once notebooks are created, update the `_toc.yml` file to include them in the book structure. Then build the book with:

```bash
jupyter-book build notebooks/book
```

## Notes

Each subdirectory contains a README.md file describing the planned notebooks for that section.
