"""Library Loader - Loads reference library files for inventors and critics."""

import logging
from pathlib import Path

logger = logging.getLogger(__name__)


# Default library mapping to files in docs/updated-docs/
DEFAULT_LIBRARY_MAP = {
    "first_principles": "First_Principles_Library_Set1 1.md",
    "mental_models": "Mental_Models_Library_v15 1.md",
    "technologies": "Technologies_Library_v1 1.md",
    "methodologies": "Inventors Toolkit (Machine Readable) 1.md",
    "secrets": "",  # No default secrets file - user-provided
    "observations": "",  # No default observations file - user-provided
}

# All known library names
ALL_LIBRARY_NAMES = list(DEFAULT_LIBRARY_MAP.keys())


class LibraryLoader:
    """Loads markdown library files for use by inventors and critics."""

    def __init__(self, base_dir: str | Path | None = None, user_paths: list[str] | None = None):
        """Initialize library loader.

        Args:
            base_dir: Base directory for default library files.
            user_paths: Additional user-provided library file paths.
        """
        if base_dir:
            self.base_dir = Path(base_dir)
        else:
            # Find docs/updated-docs/ relative to project root
            self.base_dir = self._find_library_dir()

        self.user_paths = user_paths or []
        self._cache: dict[str, str] = {}

    def _find_library_dir(self) -> Path:
        """Find the library directory relative to project root."""
        cwd = Path.cwd()
        current = cwd
        for _ in range(5):
            check = current / "docs" / "updated-docs"
            if check.exists():
                return check
            if (current / "pyproject.toml").exists():
                return current / "docs" / "updated-docs"
            if current.parent == current:
                break
            current = current.parent
        return cwd / "docs" / "updated-docs"

    def load(self, name: str) -> str:
        """Load a single library by name.

        Args:
            name: Library name (e.g. 'first_principles', 'mental_models').

        Returns:
            Library content as string, or empty string if not found.
        """
        if name in self._cache:
            return self._cache[name]

        content = self._load_from_user_paths(name)
        if not content:
            content = self._load_from_defaults(name)

        self._cache[name] = content
        if content:
            logger.info(f"Library '{name}' loaded — {len(content)} chars")
        else:
            logger.info(f"Library '{name}' not found or empty")
        return content

    def load_multiple(self, names: list[str]) -> dict[str, str]:
        """Load multiple libraries by name.

        Args:
            names: List of library names.

        Returns:
            Dict of name -> content.
        """
        return {name: self.load(name) for name in names}

    def get_all(self) -> dict[str, str]:
        """Load all available libraries.

        Returns:
            Dict of name -> content for all libraries with content.
        """
        all_libs = {}
        for name in ALL_LIBRARY_NAMES:
            content = self.load(name)
            if content:
                all_libs[name] = content

        # Also load any user-provided files not matching default names
        for path_str in self.user_paths:
            path = Path(path_str)
            if path.exists() and path.suffix.lower() in (".md", ".txt"):
                name = path.stem.lower().replace(" ", "_")
                if name not in all_libs:
                    try:
                        all_libs[name] = path.read_text(encoding="utf-8")
                    except Exception:
                        pass

        return all_libs

    def get_available_names(self) -> list[str]:
        """Get names of all available libraries (those with actual content)."""
        return [name for name in ALL_LIBRARY_NAMES if self.load(name)]

    def _load_from_user_paths(self, name: str) -> str:
        """Try to load a library from user-provided paths."""
        name_lower = name.lower().replace("_", " ")
        for path_str in self.user_paths:
            path = Path(path_str)
            if not path.exists():
                continue
            stem_lower = path.stem.lower().replace("_", " ")
            if name_lower in stem_lower or stem_lower in name_lower:
                try:
                    return path.read_text(encoding="utf-8")
                except Exception:
                    continue
        return ""

    def _load_from_defaults(self, name: str) -> str:
        """Try to load a library from the default directory."""
        filename = DEFAULT_LIBRARY_MAP.get(name, "")
        if not filename:
            return ""

        filepath = self.base_dir / filename
        if not filepath.exists():
            # Also check in the Infopack subdirectory
            for subdir in self.base_dir.iterdir():
                if subdir.is_dir():
                    candidate = subdir / filename
                    if candidate.exists():
                        filepath = candidate
                        break

        if filepath.exists():
            try:
                return filepath.read_text(encoding="utf-8")
            except Exception:
                return ""
        return ""
