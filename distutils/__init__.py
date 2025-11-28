"""Compatibility shim for environments where stdlib 'distutils' is missing.

This package forwards common submodules to setuptools' internal
`_distutils` implementation so libraries that `import distutils` (like
`packaging`) keep working on Python versions that removed stdlib
`distutils` (3.12+).

This is a temporary workaround — recommended long-term fix is to use
Python 3.11 for this project.
"""

try:
    # setuptools exposes a vendored copy at setuptools._distutils
    from setuptools import _distutils as _d
except Exception:
    # Fallback: try to import distutils normally (if available)
    try:
        import distutils as _d
    except Exception:
        _d = None

if _d is not None:
    # Export common attributes
    for _name in dir(_d):
        if not _name.startswith("_"):
            globals()[_name] = getattr(_d, _name)
