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
            host  = subprocess.getoutput(sruncmd).split()[-1]
            assert host, f"SLURM job not created. Run srun on {config['gateway']}."
    return host


def run(args: Namespace) -> None:
    config = get_config()[args.config]
    host = _get_host(config, verbose=args.verbose, dry_run=args.dry_run)
    srcdir = Path(config["deployment_path"])
    prodir = srcdir / args.directory
    devdir = prodir / ".devcontainer"
    with tempfile.TemporaryDirectory() as tmpdir:
        tmpdir = Path(tmpdir)
        shutil.copytree(_get_template_dir(), tmpdir, dirs_exist_ok=True)
        with open(tmpdir / "devcontainer.json", "r") as stream:
            devcontainer = json.load(stream)
        devcontainer["image"] = f"{args.base_image}-devcontainer"
        devcontainer["mounts"] += [
            f"source={x},target={x},type=bind,consistency=cached"
            for x in [srcdir] + args.mount
        ]
        devcontainer["initializeCommand"] = (
            f"docker inspect {args.base_image}-devcontainer 1>/dev/null"
            f" || docker build"
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
        syncmd = f"rsync -a {tmpdir}/ {f'{host}:' if host else ''}{devdir}/"
        runcmd = (
            f"code --folder-uri"
            f" {f'vscode-remote://ssh-remote+{host}' if host else ''}{prodir}"
        )
        if args.verbose or args.dry_run:
            print(syncmd)
        if not args.dry_run:
            subprocess.check_call(syncmd, shell=True)
        if args.verbose or args.dry_run:
            print(runcmd)
        if not args.dry_run:
            subprocess.check_call(runcmd, shell=True)


def explore(args: Namespace) -> None:
    config = get_config()[args.config]
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
