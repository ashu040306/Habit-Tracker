from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_tests.utils.config_reader import ConfigReader


config = ConfigReader()


def test_add_habit():

    driver = webdriver.Chrome()

    driver.get(config.get("base_url"))

    name_input = driver.find_element(By.NAME, "name")
    name_input.send_keys("Drink Water")

    description_input = driver.find_element(By.NAME, "description")
    description_input.send_keys("Drink 2 liters of water")

    add_button = driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    )

    add_button.click()

    wait = WebDriverWait(driver, 10)

    habit = wait.until(
        EC.presence_of_element_located(
            (By.CLASS_NAME, "habit-name")
        )
    )

    assert habit.text == "Drink Water"

    driver.quit()


def test_complete_habit():

    driver = webdriver.Chrome()

    driver.get(config.get("base_url"))

    # Add habit
    name_input = driver.find_element(By.NAME, "name")
    name_input.send_keys("Exercise")

    description_input = driver.find_element(By.NAME, "description")
    description_input.send_keys("30 minutes exercise")

    add_button = driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    )

    add_button.click()

    wait = WebDriverWait(driver, 10)

    # Wait for fresh Complete button
    complete_button = wait.until(
        EC.element_to_be_clickable(
            (By.CLASS_NAME, "js-complete")
        )
    )

    complete_button.click()

    # Handle JavaScript prompt
    alert = wait.until(
        EC.alert_is_present()
    )

    alert.send_keys("Completed today's exercise")
    alert.accept()

    assert "HabitTracker" in driver.title

    driver.quit()


def test_delete_habit():

    driver = webdriver.Chrome()

    driver.get(config.get("base_url"))

    # Add habit
    name_input = driver.find_element(By.NAME, "name")
    name_input.send_keys("Delete Me")

    description_input = driver.find_element(By.NAME, "description")
    description_input.send_keys("This habit will be deleted")

    add_button = driver.find_element(
        By.CSS_SELECTOR,
        "button[type='submit']"
    )

    add_button.click()

    wait = WebDriverWait(driver, 10)

    # Find the specific habit card
    habit_card = wait.until(
        EC.presence_of_element_located(
            (
                By.XPATH,
                "//h3[text()='Delete Me']/ancestor::article"
            )
        )
    )

    # Find Delete button inside that card
    delete_button = habit_card.find_element(
        By.CSS_SELECTOR,
        "button.danger"
    )

    delete_button.click()

    # Wait for old card to disappear
    wait.until(
        EC.staleness_of(habit_card)
    )

    # Get remaining habits
    habits = driver.find_elements(
        By.CLASS_NAME,
        "habit-name"
    )

    habit_names = [habit.text for habit in habits]

    assert "Delete Me" not in habit_names

    driver.quit()