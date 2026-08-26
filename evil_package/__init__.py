"""evil_package: harmless DEMO sample for dependency-sandbox testing.

Importing this module is completely inert: it does nothing and triggers
nothing. The demo payload lives only in setup.py, inside a custom
setuptools install command, and runs only during setup.py install.
"""

__version__ = "0.0.1"


def noop():
    """No-op placeholder. Does nothing, returns None."""
    return None
