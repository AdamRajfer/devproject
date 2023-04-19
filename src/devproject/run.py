import os
import subprocess
from argparse import Namespace

from devproject.utils import get_config, get_host, get_template_dir


def run(args: Namespace) -> None:
    config = get_config()[args.config]
    host = get_host(config)
    deployment = config["deployment_path"].rstrip("/")
    directory = f"{deployment}/.devprojects/{args.project}"
    devcontainer = f"{directory}/.devcontainer"
    makedirs_cmd = f"mkdir -p {devcontainer}/"
    sync_cmd = f"rsync -a {get_template_dir()}/"
    replace_cmd = (
        f"sed -i"
        f" -e 's#SRC_DIR#{deployment}#g'"
        f" -e 's#SRC_IMAGE#{args.base_image}#g'"
        f" -e 's#SRC_UID#$(id -u)#g'"
        f" -e 's#SRC_GID#$(id -g)#g'"
        f" -e 's#SRC_DOCKER#$(stat -c %g /var/run/docker.sock)#g'"
        f" {devcontainer}/*"
    )
    build_cmd = (
        f"docker build --build-arg FROM_IMAGE={args.base_image}"
        f" --build-arg USER=$(id -un) -t {args.base_image}-dev"
        f" {devcontainer}/ && rm {devcontainer}/Dockerfile && "
        f" mv {devcontainer}/devcontainer.json"
        f" {devcontainer}/../.devcontainer.json && rm -r {devcontainer}"
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
    cmd = " \\\n&& ".join([makedirs_cmd, sync_cmd, replace_cmd, build_cmd, run_cmd])
    print(cmd)
    subprocess.check_call(cmd, shell=True)
