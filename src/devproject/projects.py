import glob
import os

import pandas as pd
from tabulate import tabulate

from devproject.utils import COLUMNS, MAX_COL_WIDTHS, get_local_dir


def projects() -> None:
    dfs = [
        pd.read_csv(os.path.join(path, ".devinfo.csv"), index_col=0).squeeze()
        for path in glob.glob(f"{get_local_dir()}/*")
    ]
    if dfs:
        df = pd.concat(dfs, axis=1).T.fillna("-")
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
