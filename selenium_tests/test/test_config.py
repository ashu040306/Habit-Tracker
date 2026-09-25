from selenium_tests.utils.config_reader import ConfigReader


config = ConfigReader()

print("Browser:", config.get("browser"))
print("Base URL:", config.get("base_url"))
print("Timeout:", config.get("timeout"))