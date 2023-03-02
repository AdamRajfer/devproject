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
        workspace = f"/workspaces/{args.name}"
        args.workdir = (
            os.path.join(workspace, args.workdir)
            if args.workdir else workspace
        ).rstrip("/")
        os.makedirs(dev_dir)
        shutil.copy(f"{get_template_dir()}/settings.json", f"{dev_dir}/")
        shutil.copy(f"{get_template_dir()}/.bashrc", f"{dev_dir}/")
        shutil.copy(f"{get_template_dir()}/.profile", f"{dev_dir}/")
        with open(f"{get_template_dir()}/Dockerfile", "r") as f_src:
            with open(f"{dev_dir}/Dockerfile", "w") as f_out:
                f_out.write(f_src.read(
                    ).replace("SRC_IMAGE", args.base_image
                    ).replace("SRC_WORKDIR", args.workdir
                    ).replace("SRC_GIT_USER", get_git_username()
                    ).replace("SRC_GIT_EMAIL", get_git_useremail()
                    ).replace("SRC_WORKSPACE", workspace))
        with open(f"{get_template_dir()}/devcontainer.json", "r") as f_src:
            with open(f"{dev_dir}/devcontainer.json", "w") as f_out:
                devcontainer = json.load(f_src)
                devcontainer["workspaceFolder"] = args.workdir
                devcontainer["remoteUser"] = "SRC_USER"
                devcontainer["containerUser"] = "SRC_USER"
                cmd = f"cd {workspace}; sudo rmdir -p {args.workdir}"
                if args.git:
                    cmd = (
                        f"{cmd}; git clone {args.git} .devtmp; shopt -s " \
                        f"dotglob; mv .devtmp/* .; rm .devlock; touch " \
                        f".devtmp/.devlock"
                    )
                else:
                    cmd = f"{cmd}; mkdir -p {args.workdir}"
                if args.install_req:
                    cmd = (
                        f"{cmd}; pip install $(python -c 'import subprocess;" \
                        f" print(\"\".join([f\" -r {{x}}\" for x in" \
                        f" subprocess.getoutput(\"find {args.workdir}" \
                        f" -maxdepth {args.req_depth} -name" \
                        f" requirements.txt\").split()]))')"
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
        df = pd.Series(dict(**vars(args), datetime=datetime.now()))[COLUMNS]
        df.to_csv(f"{dev_dir}/../.devinfo.csv")
        df = df.to_frame().fillna("-").T
        df.columns = [f"\033[93m{x}\033[0m" for x in COLUMNS]
        maxcolwidths = MAX_COL_WIDTHS
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
                [[""] * len(COLUMNS)], columns=COLUMNS, index=[""]
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
