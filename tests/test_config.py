import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from config_reader import load_config, ConfigError


class TestConfigReader(unittest.TestCase):

    def _create_temp_json(self, data: dict) -> str:
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(data, file)
        return path

    def test_valid_config(self):
        data = {
            "package_name": "test",
            "repo_url": "http://test.com",
            "test_mode": True,
            "package_version": "1.0",
            "max_depth": 5
        }
        path = self._create_temp_json(data)
        config = load_config(path)
        self.assertEqual(config["max_depth"], 5)
        os.remove(path)

    def test_missing_file(self):
        with self.assertRaises(ConfigError):
            load_config("non_existent_file.json")

    def test_missing_key(self):
        data = {"package_name": "test"}
        path = self._create_temp_json(data)
        with self.assertRaises(ConfigError):
            load_config(path)
        os.remove(path)

    def test_invalid_depth(self):
        data = {
            "package_name": "test",
            "repo_url": "http://test.com",
            "test_mode": True,
            "package_version": "1.0",
            "max_depth": -1
        }
        path = self._create_temp_json(data)
        with self.assertRaises(ConfigError):
            load_config(path)
        os.remove(path)


if __name__ == "__main__":
    unittest.main()