import subprocess
from argparse import Namespace

from devproject.utils import get_config, get_user


def dev_open(args: Namespace) -> None:
    config = get_config()[args.config]
    if config["host"] == "sync":
        config["host"] = subprocess.getoutput(
            f"ssh {config['gateway']} 'HOST=$(squeue -u $USER --states R" \
            f" -O nodelist --noheader | head -n 1); echo $HOST'"
        )
    assert not subprocess.call([
        "code",
        "--folder-uri",
        f"vscode-remote://ssh-remote+{get_user()}@{config['host']}" \
        f"{args.directory}",
    ])
