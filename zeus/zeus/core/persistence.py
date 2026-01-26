"""Persistence - RunRecord storage."""

import json
import os
from pathlib import Path
from datetime import datetime
from zeus.models.schemas import RunRecord


class Persistence:
    """Handles RunRecord storage (append-only)."""

    DEFAULT_DIR = "run_records"

    def __init__(self, base_dir: str | Path | None = None):
        """Initialize persistence with storage directory.

        Args:
            base_dir: Directory for storing run records. Defaults to ./run_records/
        """
        self.base_dir = Path(base_dir) if base_dir else Path(self.DEFAULT_DIR)
        self._ensure_dir()

    def _ensure_dir(self) -> None:
        """Ensure storage directory exists."""
        self.base_dir.mkdir(parents=True, exist_ok=True)

    def save(self, record: RunRecord) -> Path:
        """Save a run record to disk (append-only).

        Args:
            record: The RunRecord to save.

        Returns:
            Path to the saved file.
        """
        # Generate filename with timestamp for ordering
        timestamp = datetime.fromisoformat(record.timestamp).strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{record.run_id[:8]}.json"
        filepath = self.base_dir / filename

        # Serialize and save
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(record.model_dump(), f, indent=2, ensure_ascii=False)

        return filepath

    def load(self, run_id: str) -> RunRecord | None:
        """Load a run record by ID.

        Args:
            run_id: The run ID to load.

        Returns:
            The RunRecord if found, None otherwise.
        """
        # Search for file matching run_id
        for filepath in self.base_dir.glob("*.json"):
            if run_id[:8] in filepath.name:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return RunRecord.model_validate(data)
        return None

    def list_runs(self, limit: int = 50) -> list[dict]:
        """List recent runs with summary info.

        Args:
            limit: Maximum number of runs to return.

        Returns:
            List of run summaries (id, timestamp, mode, status).
        """
        runs = []
        filepaths = sorted(self.base_dir.glob("*.json"), reverse=True)

        for filepath in filepaths[:limit]:
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    runs.append({
                        "run_id": data.get("run_id", "unknown"),
                        "timestamp": data.get("timestamp", "unknown"),
                        "mode": data.get("mode", "unknown"),
                        "has_response": data.get("final_response") is not None,
                        "errors": len(data.get("errors", [])),
                    })
            except (json.JSONDecodeError, KeyError):
                continue

        return runs

    def get_filepath(self, run_id: str) -> Path | None:
        """Get the filepath for a run record.

        Args:
            run_id: The run ID.

        Returns:
            Path if found, None otherwise.
        """
        for filepath in self.base_dir.glob("*.json"):
            if run_id[:8] in filepath.name:
                return filepath
        return None
