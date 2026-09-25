# HabitTracker – Test Cases

| TC ID | Module | Test Case | Preconditions | Test Steps | Expected Result | Status |
|---|---|---|---|---|---|---|
| TC-001 | Homepage | Verify homepage loads | Flask application is running | Open `http://localhost:5000` | HabitTracker homepage is displayed | Pass |
| TC-002 | Add Habit | Add a new habit with name and description | Homepage is open | Enter habit name and description → Click **Add Habit** | New habit appears on the homepage | Pass |
| TC-003 | Add Habit | Verify habit name is required | Homepage is open | Leave name empty → Click **Add Habit** | Habit is not added and validation/message is shown | Not Executed |
| TC-004 | Complete Habit | Complete an existing habit | At least one habit exists | Click **Complete** → Enter optional remark → Accept prompt | Habit is marked completed and completion is recorded | Pass |
| TC-005 | Delete Habit | Delete an existing habit | At least one habit exists | Click **Delete** on a habit | Habit is removed from the list | Pass |
| TC-006 | History | Verify completion history page | Application is running | Open `/history` | Completion History page is displayed | Pass |
| TC-007 | History | Verify completed habit appears in history | A habit has been completed | Open `/history` | Completed habit, time, and remark are displayed | Not Executed |
| TC-008 | Motivation | Verify motivation page loads | Application is running | Open `/motivation` | Motivation page is displayed | Pass |
| TC-009 | Motivation | Verify speech buttons are displayed | Motivation page is open | Inspect speech cards | Play buttons are displayed for motivational speeches | Pass |
| TC-010 | Navigation | Verify application navigation | Application is running | Navigate between Home, History and Motivation | Correct pages open without errors | Not Executed |
| TC-011 | Theme | Verify theme toggle | Homepage is open | Click theme toggle | Application theme changes | Not Executed |
| TC-012 | UI | Verify habit card information | At least one habit exists | Inspect habit card | Name, description, streak, actions and last-completed information are displayed correctly | Not Executed |
