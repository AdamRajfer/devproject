from argparse import Namespace

import pandas as pd
from tabulate import tabulate

from devproject.utils import get_config, save_config


def config(args: Namespace) -> None:
    try:
        config = get_config()
    except FileNotFoundError:
        config = {}
    if args.name:
        if args.rm:
            config.pop(args.name)
            for i, k in enumerate(config):
                config[k]["active"] = "True" if i == 0 else "False"
        else:
            if args.name not in config:
                assert args.deployment_path
                config[args.name] = {
                    "name": args.name,
                    "deployment_path": str(args.deployment_path),
                    "gateway": args.gateway,
                    "host": "sync" if args.sync_host else args.gateway,
                    "active": "True",
                }
            for k in config:
                config[k]["active"] = "True" if k == args.name else "False"
    save_config(config)
    columns = ["name", "deployment_path", "gateway", "host", "active"]
    config = (
        pd.DataFrame(config).T[columns] if config
        else pd.DataFrame(columns=columns)
    ).fillna("-")
    is_active = config["active"].apply(eval)
    config[is_active] = config[is_active].squeeze().apply(
        lambda x: f"\033[92m{x}\033[0m"
    ).tolist()
    config.columns = [f"\033[93m{x}\033[0m" for x in config.columns]
    config = config.reset_index(drop=True)
    config.index += 1
    config.index = [f"\033[96m{x}\033[0m" for x in config.index]
    print(tabulate(
        config,
        headers="keys",
        tablefmt="fancy_grid",
        rowalign="center",
        stralign="center",
        numalign="center",
        showindex=True,
    ))
