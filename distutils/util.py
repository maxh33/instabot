"""Compatibility shim for distutils.util submodule."""

try:
    # Forward all exports from setuptools._distutils.util
    from setuptools._distutils.util import *
except ImportError:
    # Fallback to stdlib distutils if available (Python < 3.12)
    try:
        from distutils.util import *
    except ImportError:
        pass
