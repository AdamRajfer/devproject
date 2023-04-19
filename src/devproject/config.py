import json
import os
from argparse import Namespace
from typing import Any, Dict

_CONFIG_PATH = f"{os.path.expanduser('~')}/.devconfig.json"


def _save_config(config: Dict[str, Dict[str, Any]]) -> None:
    with open(_CONFIG_PATH, "w") as stream:
        json.dump(config, stream, indent=4)
    for _, v in config.items():
        print(f"\033[92m{v}\033[0m" if v["active"] else v)


def get_config() -> Dict[str, Dict[str, Any]]:
    if not os.path.exists(_CONFIG_PATH):
        raise FileNotFoundError(
            "No deployment configuration found."
            " Run `dev config` to create one."
        )
    with open(_CONFIG_PATH, "r") as stream:
        return json.load(stream)


def get_active_config() -> str:
    return next(x["name"] for x in get_config().values() if x["active"])


def config(args: Namespace) -> None:
    try:
        config = get_config()
    except FileNotFoundError:
        config = {}
    if args.rm:
        config.pop(args.name)
        for i, k in enumerate(config):
            config[k]["active"] = i == 0
    else:
        if args.name not in config:
            assert args.deployment_path
            config[args.name] = {
                "name": args.name,
                "deployment_path": str(args.deployment_path),
                "gateway": args.gateway,
                "host": "sync" if args.sync_host else args.gateway,
                "active": True,
            }
        for k in config:
            config[k]["active"] = k == args.name
    _save_config(config)


def configs() -> None:
    try:
        config = get_config()
    except FileNotFoundError:
        config = {}
    _save_config(config)
