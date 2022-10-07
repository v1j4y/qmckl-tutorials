---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.12.0
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---


# QMCkl Tutorial


This tutorial covers some basic use cases of the QMCkl library based on the Python API. 
At this point, it is assumed that the QMCkl Python package has been successfully installed on the user machine 
or in the virtual environment. If this is not the case, feel free to follow the [installation guide](https://github.com/TREX-CoE/qmckl/blob/master/python/README.md).

## Importing QMCkl

```python
try:
    import qmckl
except ImportError:
    raise Exception("Unable to import qmckl. Please check that qmckl is properly installed.")
```
