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
        raise ConfigError(
            f"Файл конфигурации не найден: {file_path}"
        )

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            config = json.load(file)
    except json.JSONDecodeError as exc:
        raise ConfigError(
            f"Ошибка синтаксиса JSON: {exc}"
        ) from exc

    validate_config(config)
    return config


def validate_config(config: dict) -> None:
    _check_keys(config)
    _check_package_name(config["package_name"])
    _check_repo_url(config["repo_url"])
    _check_test_mode(config["test_mode"])
    _check_package_version(config["package_version"])
    _check_max_depth(config["max_depth"])


def _check_keys(config: dict) -> None:
    for key in REQUIRED_KEYS:
        if key not in config:
            raise ConfigError(
                f"Отсутствует обязательный параметр: {key}"
            )


def _check_package_name(name: str) -> None:
    if not isinstance(name, str) or not name:
        raise ConfigError(
            "Параметр 'package_name' должен быть непустой строкой."
        )


def _check_repo_url(url: str) -> None:
    if not isinstance(url, str) or not url:
        raise ConfigError(
            "Параметр 'repo_url' должен быть непустой строкой."
        )


def _check_test_mode(mode: bool) -> None:
    if not isinstance(mode, bool):
        raise ConfigError(
            "Параметр 'test_mode' должен быть логическим (true/false)."
        )


def _check_package_version(version: str) -> None:
    if not isinstance(version, str):
        raise ConfigError(
            "Параметр 'package_version' должен быть строкой."
        )


def _check_max_depth(depth: int) -> None:
    if not isinstance(depth, int):
        raise ConfigError(
            "Параметр 'max_depth' должен быть целым числом."
        )
    if depth < MIN_DEPTH or depth > MAX_DEPTH:
        raise ConfigError(
            f"Параметр 'max_depth' должен быть от {MIN_DEPTH} "
            f"до {MAX_DEPTH}."
        )