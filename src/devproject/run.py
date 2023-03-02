import os
import subprocess
from argparse import Namespace

from devproject.utils import get_config, get_local_dir


def run(args: Namespace) -> None:
    config = get_config()[args.config]
    host = config["host"]
    if host == "sync":
        host = subprocess.getoutput(
            f"ssh {config['gateway']} 'HOST=$(squeue -u $USER --states R" \
            f" -O nodelist --noheader | head -n 1); echo $HOST'"
        )
    local_dir = f"{get_local_dir()}/{args.project}"
    if not os.path.exists(local_dir):
        raise ValueError(f"Project {args.project} does not exist.")
    deployment_path = config["deployment_path"].rstrip("/")
    deployment_path_bash = deployment_path.replace("/", "\/")
    project_dir = f"{deployment_path}/.devprojects/{args.project}"
    dev_dir = f"{project_dir}/.devcontainer"
    makedirs_cmd = f"mkdir -p {dev_dir}/"
    sync_cmd = f"rsync -a {local_dir}/.devcontainer/"
    replace_cmd = (
        f"sed -i -e 's:SRC_DIR:{deployment_path_bash}:g'" \
        f" -e 's:SRC_USER:$(id -un):g' -e 's:SRC_UID:$(id -u):g'" \
        f" -e 's:SRC_GID:$(id -g):g' {dev_dir}/*"
    )
    run_cmd = "code --folder-uri"
    if host:
        makedirs_cmd = f"ssh {host} {makedirs_cmd}"
        sync_cmd = f"{sync_cmd} {host}:{dev_dir}/ --delete"
        replace_cmd = f"ssh {host} {replace_cmd}"
        run_cmd = f"{run_cmd} vscode-remote://ssh-remote+{host}{project_dir}"
    else:
        sync_cmd = f"{sync_cmd} {dev_dir}/ --delete"
        replace_cmd = f"eval '{replace_cmd}'"
        run_cmd = f"{run_cmd} {project_dir}"
    cmd = " \\\n&& ".join([makedirs_cmd, sync_cmd, replace_cmd, run_cmd])
    assert not subprocess.call(cmd, shell=True)