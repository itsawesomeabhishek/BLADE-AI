"""
Safety Log Module
Stores safety interlock decisions and action outcomes.
"""
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List


class SafetyLog:
    """Append-only log for safety interlock actions."""

    def __init__(self, log_dir: str = None):
        if log_dir is None:
            base_dir = Path.home() / "BladeAI" / "logs"
        else:
            base_dir = Path(log_dir)
        base_dir.mkdir(parents=True, exist_ok=True)
        self.log_path = base_dir / "action_safety_log.json"

    def _read_entries(self) -> List[Dict[str, Any]]:
        if not self.log_path.exists():
            return []
        try:
            with open(self.log_path, "r", encoding="utf-8") as handle:
                data = json.load(handle)
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def append(self, entry: Dict[str, Any]) -> None:
        entries = self._read_entries()
        entry_with_time = {
            "timestamp": datetime.now().isoformat(),
            **entry,
        }
        entries.append(entry_with_time)
        with open(self.log_path, "w", encoding="utf-8") as handle:
            json.dump(entries, handle, indent=2, ensure_ascii=True)
