"""Main entry point for Practice 2, Stage 1."""

import argparse
import sys

from config_reader import load_config, ConfigError


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Dependency Visualizer")
    parser.add_argument(
        "--config", 
        required=True, 
        help="Путь к JSON файлу конфигурации"
    )
    return parser.parse_args()


def main() -> None:
    """Run the application."""
    args = parse_args()
    
    try:
        config = load_config(args.config)
    except ConfigError as error:
        print(f"Ошибка конфигурации: {error}")
        sys.exit(1)
        
    print("Загруженные параметры (ключ-значение):")
    for key, value in config.items():
        print(f"{key} = {value}")


if __name__ == "__main__":
    main()