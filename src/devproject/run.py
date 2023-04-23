import json
import os
import shutil
import subprocess
import tempfile
from argparse import Namespace
from pathlib import Path
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
    srcdir = Path(config["deployment_path"])
    prodir = srcdir / ".devprojects" / args.project
    devdir = prodir / ".devcontainer"
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        shutil.copytree(_get_template_dir(), tmpdir, dirs_exist_ok=True)
        with open(tmpdir / "devcontainer.json", "r") as stream:
            devcontainer = json.load(stream)
        devcontainer["image"] = f"{args.base_image}-devcontainer"
        devcontainer["mounts"].append(
            f"source={srcdir},target={srcdir},type=bind,consistency=cached"
        )
        devcontainer["initializeCommand"] = (
            f"docker build"
            f" -t {args.base_image}-devcontainer"
            f" --build-arg FROM_IMAGE={args.base_image}"
            f" --build-arg USER=$(id -un)"
            f" --build-arg USER_UID=$(id -u)"
            f" --build-arg USER_GID=$(id -g)"
            f" --build-arg DOCKER_GID=$(stat -c %g /var/run/docker.sock)"
            f" {devdir}"
        )
        with open(tmpdir / "devcontainer.json", "w") as stream:
            json.dump(devcontainer, stream, indent=4)
        mkdcmd = f"{f'ssh {host} ' if host else ''}mkdir -p {devdir}"
        syncmd = f"rsync -a {tmpdir}/ {f'{host}:' if host else ''}{devdir}/"
        runcmd = (
            f"code --folder-uri"
            f" {f'vscode-remote://ssh-remote+{host}' if host else ''}{prodir}"
        )
        subprocess.check_call(mkdcmd, shell=True)
        subprocess.check_call(syncmd, shell=True)
        subprocess.check_call(runcmd, shell=True)


def explore(args: Namespace) -> None:
    config = get_config()[args.config]
    host = _get_host(config)
    runcmd = (
        f"code --folder-uri"
        f" {f'vscode-remote://ssh-remote+{host}' if host else ''}"
        f"{args.directory}"
    )
    subprocess.check_call(runcmd, shell=True)
