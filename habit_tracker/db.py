import sqlite3
from dataclasses import asdict
from datetime import date
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_DB_NAME = "habits.db"


def _data_dir() -> Path:
    package_root = Path(__file__).resolve().parent.parent
    return package_root / "data"


def _db_path(db_path: Optional[str] = None) -> str:
    if db_path:
        return db_path
    data_dir = _data_dir()
    data_dir.mkdir(parents=True, exist_ok=True)
    return str(data_dir / DEFAULT_DB_NAME)


def _get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    path = _db_path(db_path)
    conn = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
    conn.row_factory = sqlite3.Row
    return conn


def _row_to_dict(row: sqlite3.Row) -> Dict[str, Any]:
    return {key: row[key] for key in row.keys()} if row else {}


def init_db(db_path: Optional[str] = None) -> None:
    with _get_connection(db_path) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS habits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                last_completed TEXT,
                streak INTEGER NOT NULL DEFAULT 0
            )
            """
        )
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS completions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                habit_id INTEGER NOT NULL,
                completed_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                remark TEXT,
                FOREIGN KEY (habit_id) REFERENCES habits(id) ON DELETE CASCADE
            )
            """
        )
        conn.commit()


def add_habit(name: str, description: str = "", db_path: Optional[str] = None) -> int:
    init_db(db_path)
    with _get_connection(db_path) as conn:
        cursor = conn.execute(
            "INSERT INTO habits(name, description) VALUES (?, ?)",
            (name.strip(), description.strip() if description else None),
        )
        conn.commit()
        return cursor.lastrowid


def list_habits(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    init_db(db_path)
    with _get_connection(db_path) as conn:
        rows = conn.execute("SELECT * FROM habits ORDER BY id").fetchall()
        return [_row_to_dict(row) for row in rows]


def update_habit(
    hid: int,
    name: Optional[str],
    description: Optional[str],
    db_path: Optional[str] = None,
) -> bool:
    init_db(db_path)
    if name is None and description is None:
        return False

    fields: List[str] = []
    params: List[Any] = []
    if name is not None:
        fields.append("name = ?")
        params.append(name.strip())
    if description is not None:
        fields.append("description = ?")
        params.append(description.strip() if description else None)
    params.append(hid)

    with _get_connection(db_path) as conn:
        cursor = conn.execute(
            f"UPDATE habits SET {', '.join(fields)} WHERE id = ?",
            params,
        )
        conn.commit()
        return cursor.rowcount > 0


def complete_habit(
    hid: int,
    db_path: Optional[str] = None,
    remark: str = "",
) -> Dict[str, Any]:
    init_db(db_path)
    today = date.today().isoformat()

    with _get_connection(db_path) as conn:
        habit = conn.execute("SELECT * FROM habits WHERE id = ?", (hid,)).fetchone()
        if habit is None:
            raise ValueError(f"Habit id={hid} not found")

        streak = habit["streak"] or 0
        last_completed = habit["last_completed"]
        if last_completed == today:
            return {"message": "Already completed today", "id": hid, "streak": streak}

        streak += 1
        conn.execute(
            "UPDATE habits SET streak = ?, last_completed = ? WHERE id = ?",
            (streak, today, hid),
        )
        conn.execute(
            "INSERT INTO completions(habit_id, remark) VALUES (?, ?)",
            (hid, remark.strip() if remark else None),
        )
        conn.commit()

        return {"id": hid, "streak": streak}


def delete_habit(hid: int, db_path: Optional[str] = None) -> bool:
    init_db(db_path)
    with _get_connection(db_path) as conn:
        conn.execute("DELETE FROM completions WHERE habit_id = ?", (hid,))
        cursor = conn.execute("DELETE FROM habits WHERE id = ?", (hid,))
        conn.commit()
        return cursor.rowcount > 0


def get_completions(db_path: Optional[str] = None) -> List[Dict[str, Any]]:
    init_db(db_path)
    with _get_connection(db_path) as conn:
        rows = conn.execute(
            """
            SELECT
                completions.id,
                completions.habit_id,
                completions.completed_at,
                completions.remark,
                habits.name AS habit_name
            FROM completions
            JOIN habits ON habits.id = completions.habit_id
            ORDER BY completions.completed_at DESC
            """
        ).fetchall()
        return [_row_to_dict(row) for row in rows]
