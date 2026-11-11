import argparse
import sys

from config_reader import load_config, ConfigError
from dependency_parser import get_dependencies


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Dependency Visualizer")
    parser.add_argument(
        "--config", 
        required=True, 
        help="Путь к JSON файлу конфигурации"
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    
    try:
        config = load_config(args.config)
    except ConfigError as error:
        print(f"Ошибка конфигурации: {error}")
        sys.exit(1)
        
    print("Загруженные параметры (ключ-значение):")
    for key, value in config.items():
        print(f"{key} = {value}")
        
    print("\nПолучение прямых зависимостей...")
    
    try:
        deps = get_dependencies(
            repo_url=config["repo_url"],
            test_mode=config["test_mode"]
        )
        print(f"Прямые зависимости пакета {config['package_name']}:")
        for dep in deps:
            print(f" - {dep}")
    except Exception as error:
        print(f"Ошибка получения зависимостей: {error}")
        sys.exit(1)


if __name__ == "__main__":
    main()