"""
LifeOS Database Backup & System Snapshot Service
"""

import os
import shutil
from datetime import datetime
from typing import Dict, Any

class BackupService:
    """
    Automates SQLite database backup snapshots and integrity checks.
    """

    @staticmethod
    def create_database_backup(db_path: str, backup_dir: str) -> Dict[str, Any]:
        """Creates a timestamped snapshot of the SQLite database file."""
        if not os.path.exists(db_path):
            return {"success": False, "error": "Source database file does not exist."}

        os.makedirs(backup_dir, exist_ok=True)
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"lifeos_backup_{timestamp}.db"
        dest_path = os.path.join(backup_dir, backup_filename)

        try:
            shutil.copy2(db_path, dest_path)
            file_size = os.path.getsize(dest_path)
            return {
                "success": True,
                "backup_filename": backup_filename,
                "backup_path": dest_path,
                "file_size_bytes": file_size,
                "created_at": datetime.utcnow().isoformat()
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
