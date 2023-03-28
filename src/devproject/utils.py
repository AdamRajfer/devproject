import json
import os
import subprocess
from typing import Any, Dict, Optional

import pandas as pd
from tabulate import tabulate

CONFIG_PATH = f"{os.path.expanduser('~')}/.devprojects/.config.json"
COLUMNS = ["name", "base_image", "workdir", "mount", "datetime"]
MAX_COL_WIDTHS = [25, 25, 25, 25, 25]


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
    columns = ["name", "deployment_path", "gateway", "host", "active"]
    config_df = (
        pd.DataFrame(config).T[columns] if config
        else pd.DataFrame(columns=columns)
    ).fillna("-")
    is_active = config_df["active"].apply(eval)
    config_df[is_active] = config_df[is_active].squeeze().apply(
        lambda x: f"\033[92m{x}\033[0m"
    ).tolist()
    config_df.columns = [f"\033[93m{x}\033[0m" for x in config_df.columns]
    config_df = config_df.reset_index(drop=True)
    config_df.index += 1
    config_df.index = [f"\033[96m{x}\033[0m" for x in config_df.index]
    print(tabulate(
        config_df,
        headers="keys",
        tablefmt="fancy_grid",
        rowalign="center",
        stralign="center",
        numalign="center",
        showindex=True,
    ))
