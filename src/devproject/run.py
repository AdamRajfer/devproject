import os
import subprocess
from argparse import Namespace

from devproject.utils import get_config, get_local_dir, get_user


def run(args: Namespace) -> None:
    config = get_config()[args.config]
    if config["host"] == "sync":
        # TODO: Connect with interactive host only (run with /bin/bash)
        config["host"] = subprocess.getoutput(
            f"ssh {config['gateway']} 'HOST=$(squeue -u $USER --states R" \
            f" -O nodelist --noheader | head -n 1); echo $HOST'"
        )
    remote_src_dir = config["deployment_path"].rstrip("/")
    remote_src_dir_bash = remote_src_dir.replace('/', '\/')
    remote_dir = f"{remote_src_dir}/.devprojects"
    if not os.path.exists(f"{get_local_dir()}/{args.project}"):
        raise ValueError(f"Project {args.project} does not exist.")
    if config["host"]:
        assert not subprocess.call(
            f"ssh {get_user()}@{config['host']}" \
            f" mkdir -p {remote_dir}/{args.project}/.devcontainer/",
            shell=True,
        )
        assert not subprocess.call(
            f"rsync -a" \
            f" {get_local_dir()}/{args.project}/.devcontainer/" \
            f" {get_user()}@{config['host']}:" \
            f"{remote_dir}/{args.project}/.devcontainer/ --delete",
            shell=True,
        )
        assert not subprocess.call(
            f"ssh {get_user()}@{config['host']} sed -i" \
            f" -e 's:SRC_DIR:{remote_src_dir_bash}:g'" \
            f" -e 's:SRC_USER:$(id -un):g'" \
            f" -e 's:SRC_UID:$(id -u):g'" \
            f" -e 's:SRC_GID:$(id -g):g'" \
            f" {remote_dir}/{args.project}/.devcontainer/*",
            shell=True,
        )
        assert not subprocess.call(
            f"code --folder-uri" \
            f" vscode-remote://ssh-remote+{get_user()}@{config['host']}" \
            f"{remote_dir}/{args.project}",
            shell=True,
        )
    else:
        assert not subprocess.call(
            f"mkdir -p {remote_dir}/{args.project}/.devcontainer/", shell=True
        )
        assert not subprocess.call(
            f"rsync -a" \
            f" {get_local_dir()}/{args.project}/.devcontainer/" \
            f" {remote_dir}/{args.project}/.devcontainer/ --delete",
            shell=True,
        )
        assert not subprocess.call(
            f"eval 'sed -i" \
            f" -e 's:SRC_DIR:{remote_src_dir_bash}:g'" \
            f" -e 's:SRC_USER:$(id -un):g'" \
            f" -e 's:SRC_UID:$(id -u):g'" \
            f" -e 's:SRC_GID:$(id -g):g'" \
            f" {remote_dir}/{args.project}/.devcontainer/*'",
            shell=True,
        )
        assert not subprocess.call(
            f"code --folder-uri {remote_dir}/{args.project}", shell=True
        )
