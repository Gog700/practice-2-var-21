"""Unit tests for configuration reader."""

import json
import os
import sys
import tempfile
import unittest

# Добавляем папку src в путь, чтобы импортировать config_reader
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from config_reader import load_config, ConfigError  # noqa: E402


class TestConfigReader(unittest.TestCase):
    """Tests for load_config and validation."""

    def _create_temp_json(self, data: dict) -> str:
        """Helper to create a temporary JSON file."""
        fd, path = tempfile.mkstemp(suffix=".json")
        with os.fdopen(fd, "w", encoding="utf-8") as file:
            json.dump(data, file)
        return path

    def test_valid_config(self):
        """Valid config loads without errors."""
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
        """Raise error if file does not exist."""
        with self.assertRaises(ConfigError):
            load_config("non_existent_file.json")

    def test_missing_key(self):
        """Raise error if a required key is missing."""
        data = {"package_name": "test"}
        path = self._create_temp_json(data)
        with self.assertRaises(ConfigError):
            load_config(path)
        os.remove(path)

    def test_invalid_depth(self):
        """Raise error if depth is out of bounds."""
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