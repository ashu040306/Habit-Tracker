## Selenium Automation Tests

This project also contains Selenium + Pytest automation tests for the HabitTracker web application.

### Test structure

```text
selenium_tests/
├── __init__.py
├── config/
│   └── config.properties
├── utils/
│   ├── __init__.py
│   └── config_reader.py
└── test/
    ├── test_homepage.py
    ├── test_habit.py
    ├── test_history.py
    └── test_motivation.py
```

### Configuration

`selenium_tests/config/config.properties`

```properties
browser=chrome
base_url=http://localhost:5000
timeout=10
```

### Run the application

In one terminal:

```powershell
python -m flask --app habit_tracker.web run --host=localhost --port=5000
```

### Run Selenium tests

From the HabitTracker project root:

```powershell
python -m pytest selenium_tests/test -v
```

### Test coverage

- Homepage verification
- Add habit
- Complete habit
- Delete habit
- Completion history
- Motivation page
- Basic UI/page verification

Test cases and bug documentation are available in:

- `docs/TEST_CASES.md`
- `docs/BUG_REPORT.md`
