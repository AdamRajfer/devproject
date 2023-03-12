from devproject.utils import get_config, save_config


def configs() -> None:
    try:
        config = get_config()
    except FileNotFoundError:
        config = {}
    save_config(config)
