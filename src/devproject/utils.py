import json
import os
from typing import Dict

CONFIG_PATH = f"{os.path.expanduser('~')}/.devprojects/.config.json"


def get_git_username() -> str:
    username = f"'{os.popen('git config user.name').read().strip()}'"
    assert username
    return username


def get_git_useremail() -> str:
    useremail = f"'{os.popen('git config user.email').read().strip()}'"
    assert useremail
    return useremail


def get_local_dir() -> str:
    return f"{os.path.expanduser('~')}/.devprojects"


def get_template_dir() -> str:
    return f"{os.path.dirname(os.path.abspath(__file__))}/data"


def get_config() -> Dict[str, Dict[str, str]]:
    if not os.path.exists(CONFIG_PATH):
        raise FileNotFoundError(
            "No deployment configuration found." \
            " Run `dev config` to create one."
        )
    with open(CONFIG_PATH, "r") as stream:
        return json.load(stream)


def save_config(config: Dict[str, Dict[str, str]]) -> None:
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as stream:
        json.dump(config, stream, indent=4)
