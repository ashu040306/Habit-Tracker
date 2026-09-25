from selenium import webdriver

from selenium_tests.utils.config_reader import ConfigReader


config = ConfigReader()


def test_homepage():

    driver = webdriver.Chrome()

    driver.get(config.get("base_url"))

    print("Page title:", driver.title)

    assert "HabitTracker" in driver.title

    driver.quit()