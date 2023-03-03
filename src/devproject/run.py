import os
import subprocess
from argparse import Namespace

from devproject.utils import get_config, get_host, get_local_dir


def run(args: Namespace) -> None:
    config = get_config()[args.config]
    host = get_host(config)
    local = f"{get_local_dir()}/{args.project}"
    if not os.path.exists(local):
        raise ValueError(f"Project {args.project} does not exist.")
    deployment = config["deployment_path"].rstrip("/")
    deployment_bash = deployment.replace("/", "\/")
    directory = f"{deployment}/.devprojects/{args.project}"
    devcontainer = f"{directory}/.devcontainer"
    makedirs_cmd = f"mkdir -p {devcontainer}/"
    sync_cmd = f"rsync -a {local}/.devcontainer/"
    replace_cmd = (
        f"sed -i -e 's:SRC_DIR:{deployment_bash}:g'" \
        f" -e 's:SRC_USER:$(id -un):g' -e 's:SRC_UID:$(id -u):g'" \
        f" -e 's:SRC_GID:$(id -g):g' {devcontainer}/*"
    )
    run_cmd = "code --folder-uri"
    if host:
        makedirs_cmd = f"ssh {host} {makedirs_cmd}"
        sync_cmd = f"{sync_cmd} {host}:{devcontainer}/ --delete"
        replace_cmd = f"ssh {host} {replace_cmd}"
        run_cmd = f"{run_cmd} vscode-remote://ssh-remote+{host}{directory}"
    else:
        sync_cmd = f"{sync_cmd} {devcontainer}/ --delete"
        replace_cmd = f"eval '{replace_cmd}'"
        run_cmd = f"{run_cmd} {directory}"
    cmd = " \\\n&& ".join([makedirs_cmd, sync_cmd, replace_cmd, run_cmd])
    assert not subprocess.call(cmd, shell=True), "Bash command failed."
