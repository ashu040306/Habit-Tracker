# HabitTracker – Bug Report

## Bug Report 001

**Bug ID:** BUG-001  
**Title:** Complete button becomes stale after adding a habit  
**Module:** Habit Management / Selenium Automation  
**Severity:** Medium  
**Priority:** Medium  
**Environment:** Windows 11, Chrome, Selenium, Python 3.13, Flask  
**Status:** Fixed

### Description
After adding a new habit, Selenium may throw `StaleElementReferenceException` when attempting to click the Complete button if the element reference was obtained before the page reload completed.

### Steps to Reproduce
1. Open the HabitTracker homepage.
2. Enter a habit name such as `Exercise`.
3. Enter a description.
4. Click **Add Habit**.
5. Immediately use a previously located `.js-complete` element.
6. Attempt to click the Complete button.

### Expected Result
Selenium should locate the current Complete button after the page reload and click it successfully.

### Actual Result
Selenium throws:

`StaleElementReferenceException: stale element reference: stale element not found`

### Root Cause
The Add Habit action submits a form and reloads the page. The old DOM elements are replaced, so an element reference obtained before the reload is no longer valid.

### Resolution
Wait for the new page content and locate the Complete button again after the reload. The test was also improved to locate the Complete button inside the specific `Exercise` habit card.

### Verification
The updated Selenium test was executed successfully after applying the fix.
