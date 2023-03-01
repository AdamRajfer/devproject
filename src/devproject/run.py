import os
import subprocess
from argparse import Namespace

from devproject.utils import get_config, get_local_dir, get_user


def run(args: Namespace) -> None:
    config = get_config()[args.config]
    if config["host"] == "sync":
        config["host"] = subprocess.getoutput(
            f"ssh {config['gateway']} 'HOST=$(squeue -u $USER --states R" \
            f" -O nodelist --noheader | head -n 1); echo $HOST'"
        )
    remote_src_dir = config["deployment_path"].rstrip("/")
    remote_src_dir_bash = remote_src_dir.replace('/', '\/')
    remote_dir = f"{remote_src_dir}/.devprojects"
    if not os.path.exists(f"{get_local_dir()}/{args.project}"):
        raise ValueError(f"Project {args.project} does not exist.")
    assert not subprocess.call(
        f"rsync -a {get_local_dir()}/" \
        f" {get_user()}@{config['host']}:{remote_dir}/",
        shell=True,
    )
    assert not subprocess.call(
        f"ssh {get_user()}@{config['host']} sed -i" \
        f" -e 's:SRC_DIR:{remote_src_dir_bash}:g'" \
        f" -e 's:SRC_USER:$(id -un):g'" \
        f" -e 's:SRC_UID:$(id -u):g'" \
        f" -e 's:SRC_GID:$(id -g):g'" \
        f" {remote_dir}/*/.devcontainer/*",
        shell=True,
    )
    assert not subprocess.call(
        f"code --folder-uri" \
        f" vscode-remote://ssh-remote+{get_user()}@{config['host']}" \
        f"{remote_dir}/{args.project}",
        shell=True,
    )
