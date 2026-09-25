from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium_tests.utils.config_reader import ConfigReader


config = ConfigReader()


def test_motivation_page():

    driver = webdriver.Chrome()

    driver.get(
        config.get("base_url") + "/motivation"
    )

    wait = WebDriverWait(driver, 10)

    heading = wait.until(
        EC.presence_of_element_located(
            (By.TAG_NAME, "h2")
        )
    )

    assert heading.text == "Motivation"

    # Check speech buttons
    play_buttons = driver.find_elements(
        By.CLASS_NAME,
        "js-play"
    )

    assert len(play_buttons) > 0

    driver.quit()