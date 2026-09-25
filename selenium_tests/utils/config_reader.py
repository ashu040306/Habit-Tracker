import os


class ConfigReader:

    def __init__(self):
        self.config = {}

        base_dir = os.path.dirname(os.path.dirname(__file__))

        config_file = os.path.join(
            base_dir,
            "config",
            "config.properties"
        )

        with open(config_file, "r") as file:
            for line in file:
                line = line.strip()

                if line and not line.startswith("#"):
                    key, value = line.split("=", 1)
                    self.config[key.strip()] = value.strip()

    def get(self, key):
        return self.config.get(key)