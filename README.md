<<<<<<< HEAD
# Habit-Tracker
A Python-based Habit Tracker built using Specification-Driven Development (SDD) with SQLite for data persistence, featuring habit management, progress tracking, and a clean modular architecture.
=======
# HabitTracker (CLI)

Simple Python CLI for tracking habits with a local SQLite database.

Usage examples:

Initialize database (creates `data/habits.db`):

```bash
python -m habit_tracker init
```

Add a habit:

```bash
python -m habit_tracker add --name "Meditate" --description "10 minutes"
```

List habits:

```bash
python -m habit_tracker list
```

Mark completed:

```bash
python -m habit_tracker complete --id 1

Run the web UI (after installing dependencies):

```bash
pip install -r requirements.txt
python -m habit_tracker.web
```

Then open http://127.0.0.1:5000 in your browser.
```
>>>>>>> bbaae5d (Initial commit)
