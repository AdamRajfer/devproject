import glob
import json
import os
import shutil
from argparse import Namespace
from datetime import datetime

import pandas as pd
from tabulate import tabulate

from devproject.utils import (get_git_useremail, get_git_username,
                              get_local_dir, get_template_dir)

COLUMNS = [
    "name",
    "base_image",
    "workdir",
    "install_req",
    "req_depth",
    "git",
    "mount",
    "datetime",
]
MAX_COL_WIDTHS = [25, 25, 25, None, 25, 25, 25, 25]


def project(args: Namespace) -> None:
    if args.name:
        dev_dir = f"{get_local_dir()}/{args.name}/.devcontainer"
        if args.rm:
            shutil.rmtree(os.path.dirname(dev_dir))
            return
        elif args.base_image:
            workspace_dir = f"/workspaces/{args.name}"
            args.workdir = (
                os.path.join(workspace_dir, args.workdir) if args.workdir
                else workspace_dir
            )
            if args.workdir.endswith("/"):
                args.workdir = args.workdir[:-1]
            os.makedirs(dev_dir)
            shutil.copyfile(
                f"{get_template_dir()}/settings.json",
                f"{dev_dir}/settings.json",
            )
            shutil.copyfile(
                f"{get_template_dir()}/.bashrc", f"{dev_dir}/.bashrc"
            )
            with open(f"{dev_dir}/Dockerfile", "w") as f_out:
                f_out.write(
                    f"FROM {args.base_image}\n" \
                    f"WORKDIR {args.workdir}\n" \
                    f"RUN groupadd -o --gid SRC_GID SRC_USER \\\n" \
                    f"    && useradd --uid SRC_UID --gid SRC_GID -m SRC_USER \\\n" \
                    f"    && apt-get update \\\n" \
                    f"    && apt-get install -y sudo bash-completion \\\n" \
                    f"    && echo SRC_USER ALL=\(root\) NOPASSWD:ALL >" \
                    f" /etc/sudoers.d/SRC_USER \\\n" \
                    f"    && chmod 0440 /etc/sudoers.d/SRC_USER\n" \
                    f"USER SRC_USER\n" \
                    f"COPY .bashrc /home/SRC_USER/.bashrc\n" \
                    f"RUN pip install --upgrade pip\n" \
                    f"RUN pip install mypy pytest\n" \
                    f"RUN git config --global user.name" \
                    f" {get_git_username()}\n" \
                    f"RUN git config --global user.email" \
                    f" {get_git_useremail()}\n" \
                    f"RUN git config --global --add safe.directory" \
                    f" {workspace_dir}\n" \
                    f"RUN touch /home/SRC_USER/.gitignore\n" \
                    f"RUN echo '.devinfo.csv' >> /home/SRC_USER/.gitignore\n" \
                    f"RUN echo '.devcontainer/' >>" \
                    f" /home/SRC_USER/.gitignore\n" \
                    f"RUN echo '.devtmp/' >> /home/SRC_USER/.gitignore\n" \
                    f"RUN echo '.hypothesis/' >> /home/SRC_USER/.gitignore\n" \
                    f"RUN echo '**/__pycache__/' >>" \
                    f" /home/SRC_USER/.gitignore\n" \
                    f"RUN git config --global core.excludesfile" \
                    f" /home/SRC_USER/.gitignore\n"
                )
            with open(f"{get_template_dir()}/devcontainer.json", "r") as f_src:
                with open(f"{dev_dir}/devcontainer.json", "w") as f_out:
                    devcontainer = json.load(f_src)
                    devcontainer["workspaceFolder"] = args.workdir
                    devcontainer["remoteUser"] = "SRC_USER"
                    devcontainer["containerUser"] = "SRC_USER"
                    cmd = f"cd {workspace_dir}; sudo rmdir -p {args.workdir}"
                    if args.git:
                        cmd = (
                            f"{cmd}; git clone {args.git} .devtmp;" \
                            f" shopt -s dotglob; mv .devtmp/* .;" \
                            f" rm .devlock; touch .devtmp/.devlock"
                        )
                    else:
                        cmd = f"{cmd}; mkdir -p {args.workdir}"
                    if args.install_req:
                        cmd = (
                            f"{cmd}; pip install" \
                            f" $(python -c 'import subprocess;" \
                            f" print(\"\".join([f\" -r {{x}}\"" \
                            f" for x in subprocess.getoutput(" \
                            f"\"find {args.workdir}" \
                            f" -maxdepth {args.req_depth}" \
                            f" -name requirements.txt\").split()]))')"
                        )
                    devcontainer["postCreateCommand"] = cmd
                    if args.mount:
                        mount = (x.split(":") for x in args.mount)
                        devcontainer["mounts"] = [
                            f"source=SRC_DIR/{src},target={tgt}" \
                            f",type=bind,consistency=cached"
                            for src, tgt in mount
                        ]
                    json.dump(devcontainer, f_out, indent=4)
            df = pd.Series(
                dict(**vars(args), datetime=datetime.now())
            )[COLUMNS]
            df.to_csv(f"{dev_dir}/../.devinfo.csv")
            df = df.to_frame().fillna("-").T
            df.columns = [f"\033[93m{x}\033[0m" for x in COLUMNS]
            maxcolwidths = MAX_COL_WIDTHS
        else:
            raise ValueError("Provide `--base-image to your command.`")
    else:
        df = [
            pd.read_csv(
                os.path.join(path, ".devinfo.csv"), index_col=0
            ).squeeze()
            for path in glob.glob(f"{get_local_dir()}/*")
        ]
        if df:
            df = pd.concat(df, axis=1).T.fillna("-")
            df["datetime"] = pd.to_datetime(df["datetime"])
            df = df.sort_values(by=["datetime"]).reset_index(drop=True)
            df.index += 1
            df = df.reset_index()
            df["index"] = [f"\033[96m{x}\033[0m" for x in df["index"]]
            df = df.rename(columns={"index": " "})
            maxcolwidths = [None, *MAX_COL_WIDTHS]
        else:
            df = pd.DataFrame(
                [[""] * 7], columns=COLUMNS, index=[""]
            ).astype(str)
            maxcolwidths = MAX_COL_WIDTHS
        df.columns = [f"\033[93m{x}\033[0m" for x in df.columns]
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
