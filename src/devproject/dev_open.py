import subprocess
from argparse import Namespace

from devproject.utils import get_config, get_host


def dev_open(args: Namespace) -> None:
    config = get_config()[args.config]
    host = get_host(config)
    cmd = "code --folder-uri"
    if host:
        cmd = f"{cmd} vscode-remote://ssh-remote+{host}{args.directory}"
    else:
        cmd = f"{cmd} {args.directory}"
    subprocess.check_call(cmd, shell=True)
