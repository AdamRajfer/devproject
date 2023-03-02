import subprocess
from argparse import Namespace

from devproject.utils import get_config


def dev_open(args: Namespace) -> None:
    config = get_config()[args.config]
    host = config["host"]
    if host == "sync":
        host = subprocess.getoutput(
            f"ssh {config['gateway']} 'HOST=$(squeue -u $USER --states R" \
            f" -O nodelist --noheader | head -n 1); echo $HOST'"
        )
    assert not subprocess.call(
        f"code --folder-uri vscode-remote://ssh-remote+{host}{args.directory}",
        shell=True,
    )
