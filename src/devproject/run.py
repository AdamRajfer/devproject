import os
import subprocess
from argparse import Namespace
from typing import Any, Dict, Optional

from devproject.config import get_config


def _get_template_dir() -> str:
    return f"{os.path.dirname(os.path.abspath(__file__))}/data"


def _get_host(config: Dict[str, Any]) -> Optional[str]:
    host = config["host"]
    if host == "sync":
        host  = subprocess.getoutput(
            f"ssh {config['gateway']} 'HOST=$(squeue -u $USER --states R"
            f" -O nodelist --noheader | head -n 1); echo $HOST'"
        ).split()[-1]
        assert host, f"SLURM job not created. Run srun on {config['gateway']}."
    return host


def run(args: Namespace) -> None:
    config = get_config()[args.config]
    host = _get_host(config)
    deployment = config["deployment_path"].rstrip("/")
    directory = f"{deployment}/.devprojects/{args.project}"
    devcontainer = f"{directory}/.devcontainer"
    makedirs_cmd = f"mkdir -p {devcontainer}/"
    sync_cmd = f"rsync -a {_get_template_dir()}/"
    replace_cmd = (
        f"sed -i"
        f" -e 's#SRC_DIR#{deployment}#g'"
        f" -e 's#SRC_IMAGE#{args.base_image}#g'"
        f" {devcontainer}/*"
    )
    build_cmd = (
        f"docker build -t {args.base_image}-devcontainer"
        f" --build-arg FROM_IMAGE={args.base_image}"
        f" --build-arg USER=$(id -un)"
        f" --build-arg USER_UID=$(id -u)"
        f" --build-arg USER_GID=$(id -g)"
        f" --build-arg DOCKER_GID=$(stat -c %g /var/run/docker.sock)"
        f" {devcontainer}/"
        f" && mv {devcontainer}/devcontainer.json"
        f" {devcontainer}/../.devcontainer.json"
        f" && rm -r {devcontainer}"
    )
    run_cmd = "code --folder-uri"
    if host:
        makedirs_cmd = f"ssh {host} {makedirs_cmd}"
        sync_cmd = f"{sync_cmd} {host}:{devcontainer}/ --delete"
        replace_cmd = f"ssh {host} {replace_cmd}"
        build_cmd = f"ssh {host} '{build_cmd}'"
        run_cmd = f"{run_cmd} vscode-remote://ssh-remote+{host}{directory}"
    else:
        sync_cmd = f"{sync_cmd} {devcontainer}/ --delete"
        replace_cmd = f"eval '{replace_cmd}'"
        build_cmd = f"eval '{build_cmd}'"
        run_cmd = f"{run_cmd} {directory}"
    cmd = " \\\n&& ".join(
        [makedirs_cmd, sync_cmd, replace_cmd, build_cmd, run_cmd]
    )
    print(cmd)
    subprocess.check_call(cmd, shell=True)


def explore(args: Namespace) -> None:
    config = get_config()[args.config]
    host = _get_host(config)
    cmd = "code --folder-uri"
    if host:
        cmd = f"{cmd} vscode-remote://ssh-remote+{host}{args.directory}"
    else:
        cmd = f"{cmd} {args.directory}"
    subprocess.check_call(cmd, shell=True)
