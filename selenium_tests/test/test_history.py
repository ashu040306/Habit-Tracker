from selenium import webdriver
from selenium.webdriver.common.by import By

from selenium_tests.utils.config_reader import ConfigReader


config = ConfigReader()


def test_history_page():

    driver = webdriver.Chrome()

    driver.get(config.get("base_url"))

    # Open history page
    driver.get(
        config.get("base_url") + "/history"
    )

    # Verify page heading
    heading = driver.find_element(By.TAG_NAME, "h2")

    assert heading.text == "Completion History"

    driver.quit()