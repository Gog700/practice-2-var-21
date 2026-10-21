import json
import os

MIN_DEPTH = 0
MAX_DEPTH = 100
REQUIRED_KEYS = [
    "package_name", "repo_url", "test_mode", 
    "package_version", "max_depth"
]


class ConfigError(Exception):
    pass


def load_config(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise ConfigError(f"Файл конфигурации не найден: {file_path}")
    
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config = json.load(file)
    except json.JSONDecodeError as exc:
        raise ConfigError(f"Ошибка синтаксиса JSON: {exc}") from exc
    
    validate_config(config)
    return config


def validate_config(config: dict) -> None:
    for key in REQUIRED_KEYS:
        if key not in config:
            raise ConfigError(f"Отсутствует обязательный параметр: {key}")
            
    if not isinstance(config["package_name"], str) or not config["package_name"]:
        raise ConfigError("Параметр 'package_name' должен быть непустой строкой.")
        
    if not isinstance(config["repo_url"], str) or not config["repo_url"]:
        raise ConfigError("Параметр 'repo_url' должен быть строкой.")
        
    if not isinstance(config["test_mode"], bool):
        raise ConfigError("Параметр 'test_mode' должен быть логическим (true/false).")
        
    if not isinstance(config["package_version"], str):
        raise ConfigError("Параметр 'package_version' должен быть строкой.")
        
    if not isinstance(config["max_depth"], int):
        raise ConfigError("Параметр 'max_depth' должен быть целым числом.")
        
    if config["max_depth"] < MIN_DEPTH or config["max_depth"] > MAX_DEPTH:
        raise ConfigError(
            f"Параметр 'max_depth' должен быть в пределах "
            f"от {MIN_DEPTH} до {MAX_DEPTH}."
        )