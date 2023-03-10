import json
import os
import shutil
from argparse import Namespace
from datetime import datetime

import pandas as pd
from tabulate import tabulate

from devproject.utils import (COLUMNS, MAX_COL_WIDTHS, get_git_useremail,
                              get_git_username, get_local_dir,
                              get_template_dir)


def project(args: Namespace) -> None:
    dev_dir = f"{get_local_dir()}/{args.name}/.devcontainer"
    if args.rm:
        shutil.rmtree(os.path.dirname(dev_dir))
        return
    workspace_abs = f"/home/SRC_USER/{args.name}"
    workdir_abs = f"{workspace_abs}/{args.workdir or ''}".rstrip("/")
    os.makedirs(dev_dir)
    shutil.copy(f"{get_template_dir()}/settings.json", f"{dev_dir}/")
    shutil.copy(f"{get_template_dir()}/.bashrc", f"{dev_dir}/")
    shutil.copy(f"{get_template_dir()}/.bash_logout", f"{dev_dir}/")
    shutil.copy(f"{get_template_dir()}/.profile", f"{dev_dir}/")
    with open(f"{get_template_dir()}/Dockerfile", "r") as f_src:
        with open(f"{dev_dir}/Dockerfile", "w") as f_out:
            f_out.write(f_src.read(
                ).replace("SRC_IMAGE", args.base_image
                ).replace("SRC_WORKDIR", workdir_abs
                ).replace("SRC_GIT_USER", get_git_username()
                ).replace("SRC_GIT_EMAIL", get_git_useremail()
                ).replace("SRC_WORKSPACE", workspace_abs))
    with open(f"{get_template_dir()}/devcontainer.json", "r") as f_src:
        with open(f"{dev_dir}/devcontainer.json", "w") as f_out:
            devcontainer = json.load(f_src)
            devcontainer["workspaceFolder"] = workdir_abs
            devcontainer["workspaceMount"] = (
                f"source=${{localWorkspaceFolder}}," \
                f"target={workspace_abs},type=bind,consistency=cached"
            )
            cmd = ""
            if args.git:
                cmd = f"cd {workspace_abs}"
                if args.workdir:
                    cmd = f"{cmd}; sudo rmdir -p {args.workdir}"
                cmd = (
                    f"{cmd}; git clone {args.git} .devtmp; shopt -s dotglob;" \
                    f" mv .devtmp/* .; rm .devlock; touch .devtmp/.devlock"
                )
            if args.install_req:
                cmd = (
                    f"{cmd or cmd + '; '}pip install $(python -c 'import" \
                    f" subprocess; print(\"\".join([f\" -r {{x}}\" for x in" \
                    f" subprocess.getoutput(\"find {workdir_abs} -maxdepth" \
                    f" {args.req_depth} -name requirements.txt\").split()]))')"
                )
            if cmd:
                devcontainer["postCreateCommand"] = cmd
            if args.mount:
                mount = (x.split(":") for x in args.mount)
                devcontainer["mounts"] = [
                    f"source=SRC_DIR/{src},target={tgt}" \
                    f",type=bind,consistency=cached"
                    for src, tgt in mount
                ]
            json.dump(devcontainer, f_out, indent=4)
    df = pd.Series(dict(**vars(args), datetime=datetime.now()))[COLUMNS]
    df.to_csv(f"{dev_dir}/../.devinfo.csv")
    df = df.to_frame().fillna("-").T
    df.columns = [f"\033[93m{x}\033[0m" for x in COLUMNS]
    maxcolwidths = MAX_COL_WIDTHS
    print(tabulate(
        df,
        headers="keys",
        tablefmt="fancy_grid",
        maxcolwidths=maxcolwidths,
        rowalign="center",
        stralign="center",
        numalign="center",
        showindex=False,
    ))
