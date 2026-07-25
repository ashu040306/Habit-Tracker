"""Simple CLI for HabitTracker"""
import argparse
import sys
from typing import Optional

from . import db


def cmd_init(args: argparse.Namespace) -> int:
    db.init_db(args.db)
    print(f"Initialized database at {db._db_path(args.db)}")
    return 0


def cmd_add(args: argparse.Namespace) -> int:
    hid = db.add_habit(args.name, args.description or "", args.db)
    print(f"Added habit id={hid} name='{args.name}'")
    return 0


def cmd_list(args: argparse.Namespace) -> int:
    rows = db.list_habits(args.db)
    if not rows:
        print("No habits yet. Add one with 'add'")
        return 0
    for r in rows:
        print(f"{r['id']}: {r['name']} - {r.get('description') or ''} (streak: {r.get('streak',0)}) last: {r.get('last_completed')}")
    return 0


def cmd_complete(args: argparse.Namespace) -> int:
    try:
        res = db.complete_habit(args.id, args.db)
        if res.get("message"):
            print(res["message"]) 
        else:
            print(f"Marked habit {res['id']} complete. Streak: {res['streak']}")
        return 0
    except ValueError as e:
        print(e)
        return 2


def cmd_update(args: argparse.Namespace) -> int:
    changed = db.update_habit(args.id, args.name, args.description, args.db)
    print("Updated" if changed else "No change / not found")
    return 0


def cmd_delete(args: argparse.Namespace) -> int:
    ok = db.delete_habit(args.id, args.db)
    print("Deleted" if ok else "Not found")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="habittracker")
    p.add_argument("--db", help="Path to sqlite db", default=None)
    sub = p.add_subparsers(dest="cmd")

    sp = sub.add_parser("init", help="Initialize database")
    sp.set_defaults(func=cmd_init)

    sp = sub.add_parser("add", help="Add a new habit")
    sp.add_argument("--name", required=True)
    sp.add_argument("--description")
    sp.set_defaults(func=cmd_add)

    sp = sub.add_parser("list", help="List habits")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("complete", help="Mark a habit complete for today")
    sp.add_argument("--id", type=int, required=True)
    sp.set_defaults(func=cmd_complete)

    sp = sub.add_parser("update", help="Update habit")
    sp.add_argument("--id", type=int, required=True)
    sp.add_argument("--name")
    sp.add_argument("--description")
    sp.set_defaults(func=cmd_update)

    sp = sub.add_parser("delete", help="Delete habit")
    sp.add_argument("--id", type=int, required=True)
    sp.set_defaults(func=cmd_delete)

    return p


def main(argv: Optional[list] = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    if not hasattr(args, "func"):
        parser.print_help()
        return 1
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
