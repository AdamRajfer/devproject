import json
import os
import shutil
from argparse import Namespace
from datetime import datetime

import pandas as pd
from tabulate import tabulate

from devproject.utils import (COLUMNS, MAX_COL_WIDTHS, get_local_dir,
                              get_template_dir)


def project(args: Namespace) -> None:
    dev_dir = f"{get_local_dir()}/{args.name}/.devcontainer"
    if args.rm:
        shutil.rmtree(os.path.dirname(dev_dir))
        return
    workspace_abs = f"SRC_DIR/.devprojects-workspace/{args.name}"
    workdir_abs = f"{workspace_abs}/{args.workdir or ''}".rstrip("/")
    os.makedirs(dev_dir)
    shutil.copy(f"{get_template_dir()}/settings.json", f"{dev_dir}/")
    with open(f"{get_template_dir()}/Dockerfile", "r") as f_src:
        dockerfile = f_src.read().replace("SRC_IMAGE", args.base_image).replace("SRC_WORKDIR", workdir_abs)
    with open(f"{dev_dir}/Dockerfile", "w") as f_out:
        f_out.write(dockerfile)
    with open(f"{get_template_dir()}/devcontainer.json", "r") as f_src:
        devcontainer = json.load(f_src)
        devcontainer["workspaceFolder"] = workdir_abs
        devcontainer["workspaceMount"] = f"source=${{localWorkspaceFolder}},target={workspace_abs},type=bind,consistency=cached"
        devcontainer["mounts"] += args.mount
    with open(f"{dev_dir}/devcontainer.json", "w") as f_out:
        json.dump(devcontainer, f_out, indent=4)
    df = pd.Series(dict(**vars(args), datetime=datetime.now()))[COLUMNS]
    df.to_csv(f"{dev_dir}/../.devinfo.csv")
    df = df.to_frame().fillna("-").T
    df.columns = [f"\033[93m{x}\033[0m" for x in COLUMNS]
    print(tabulate(
        df,
        headers="keys",
        tablefmt="fancy_grid",
        maxcolwidths=MAX_COL_WIDTHS,
        rowalign="center",
        stralign="center",
        numalign="center",
        showindex=False,
    ))
