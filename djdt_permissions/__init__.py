import importlib.metadata

__version__ = ""

try:
    __version__ = importlib.metadata.version("djdt-permissions")
except:                  # pragma: no cover  This is only relevant when the package is not built.
    __version__ = "dev"  # pragma: no cover
