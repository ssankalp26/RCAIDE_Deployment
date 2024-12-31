"""Version information."""
from pathlib import Path

def get_version():
    """Get the version from the VERSION file."""
    version_file = Path(__file__).parent.parent / "VERSION"
    with open(version_file, "r", encoding="utf-8") as f:
        version = f.read().strip()
    return version

__version__ = get_version() 