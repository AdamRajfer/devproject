import json
import os
import subprocess
from argparse import Namespace
from typing import Any, Dict, Optional

CONFIG_PATH = f"{os.path.expanduser('~')}/.devprojects/.config.json"


def get_git_username() -> str:
    username = os.popen('git config user.name').read().strip()
    assert username, "Run git config --global user.name <Your Name>."
    return f"'{username}'"


def get_git_useremail() -> str:
    useremail = os.popen('git config user.email').read().strip()
    assert useremail, "Run git config --global user.email <your@email.com>."
    return f"'{useremail}'"


def get_local_dir() -> str:
    return f"{os.path.expanduser('~')}/.devprojects"


def get_template_dir() -> str:
    return f"{os.path.dirname(os.path.abspath(__file__))}/data"


def get_host(config: Dict[str, Any]) -> Optional[str]:
    host = config["host"]
    if host == "sync":
        host  = subprocess.getoutput(
            f"ssh {config['gateway']} 'HOST=$(squeue -u $USER --states R" \
            f" -O nodelist --noheader | head -n 1); echo $HOST'"
        ).split()[-1]
        assert host, f"SLURM job not created. Run srun on {config['gateway']}."
    return host


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
