"""Startup compatibility shim loaded automatically by Python when the
project root is on `PYTHONPATH`.

This patches `collections.Iterable` and `collections.Mapping` to point to
`collections.abc` equivalents on Python 3.10+ so older libraries that import
from `collections` keep working.

Place this file in the project root and ensure subprocesses set PYTHONPATH
to include the project root (the test runner already does that).
"""
import sys
import warnings
try:
    import collections
    import collections.abc
except Exception:
    # If import fails, nothing to patch
    collections = None

if collections is not None:
    if not hasattr(collections, "Iterable"):
        try:
            collections.Iterable = collections.abc.Iterable
        except Exception:
            pass
    if not hasattr(collections, "Mapping"):
        try:
            collections.Mapping = collections.abc.Mapping
        except Exception:
            pass
