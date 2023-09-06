import json
import os
import subprocess
from argparse import Namespace
from pathlib import Path
from typing import Any, Dict, Optional

_CONFIG_PATH = f"{os.path.expanduser('~')}/.devconfig.json"


def _get_config() -> Dict[str, Dict[str, Any]]:
    if not os.path.exists(_CONFIG_PATH):
        raise FileNotFoundError(
            "No deployment configuration found."
            " Run `dev config` to create one."
        )
    with open(_CONFIG_PATH, "r") as stream:
        return json.load(stream)


def _get_host(
    config: Dict[str, Any], verbose: bool = False, dry_run: bool = False
) -> Optional[str]:
    host = config["host"]
    if host == "sync":
        sruncmd = (
            f"ssh {config['gateway']} 'HOST=$(squeue -u $USER --states R"
            f" --format '%.100N' --noheader | head -n 1); echo $HOST'"
        )
        if verbose or dry_run:
            print(sruncmd)
        if dry_run:
            host = "sync"
        else:
            host = subprocess.getoutput(sruncmd).split()[-1]
            assert host, f"Run srun on {config['gateway']}."
    return host


def _save_config(config: Dict[str, Dict[str, Any]]) -> None:
    with open(_CONFIG_PATH, "w") as stream:
        json.dump(config, stream, indent=4)
    for _, v in config.items():
        print(f"\033[92m{v}\033[0m" if v["active"] else v)


def get_active_config() -> str:
    return next(x["name"] for x in _get_config().values() if x["active"])


def config(args: Namespace) -> None:
    try:
        config = _get_config()
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
        config = _get_config()
    except FileNotFoundError:
        config = {}
    _save_config(config)


def explore(args: Namespace) -> None:
    config = _get_config()[args.config]
    host = _get_host(config, verbose=args.verbose, dry_run=args.dry_run)
    srcdir = Path(config["deployment_path"])
    runcmd = (
        f"code --folder-uri"
        f" {f'vscode-remote://ssh-remote+{host}' if host else ''}"
        f"{srcdir / args.directory}"
    )
    if args.verbose or args.dry_run:
        print(runcmd)
    if not args.dry_run:
        subprocess.check_call(runcmd, shell=True)
