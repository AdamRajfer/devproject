#!/usr/bin/env python
import os
import pathlib
from argparse import (ArgumentDefaultsHelpFormatter, ArgumentParser,
                      HelpFormatter)

from devproject.config import config
from devproject.configs import configs
from devproject.dev_open import dev_open
from devproject.run import run
from devproject.utils import get_active_config


def _formater_class(prog: str) -> HelpFormatter:
    return ArgumentDefaultsHelpFormatter(
        prog, max_help_position=130, width=150
    )


def dev() -> None:
    parser = ArgumentParser(formatter_class=_formater_class, add_help=False)
    parser.add_argument("cmd", choices=["config", "configs", "run", "open"])
    args, rest = parser.parse_known_args()
    if args.cmd == "config":
        parser = ArgumentParser(formatter_class=_formater_class)
        parser.add_argument("name", type=str, help="configuration name")
        parser.add_argument(
            "--deployment-path",
            type=pathlib.Path,
            default=os.path.expanduser("~"),
            help="deployment path on the remote machine",
        )
        parser.add_argument("--gateway", type=str, help="gateway host name")
        parser.add_argument(
            "--sync-host",
            action="store_true",
            help="whether to automatically sync host",
        )
        parser.add_argument(
            "--rm",
            action="store_true",
            help="whether remove the deployment configuration",
        )
        config(parser.parse_args(rest))
    elif args.cmd == "configs":
        configs()
    elif args.cmd == "run":
        parser = ArgumentParser(formatter_class=_formater_class)
        parser.add_argument("project", type=str, help="project name")
        parser.add_argument(
            "--base-image", default="python:3", type=str, help="base image"
        )
        parser.add_argument(
            "--config",
            type=str,
            default=get_active_config(),
            help="deployment configuration",
        )
        run(parser.parse_args(rest))
    else:
        parser = ArgumentParser(formatter_class=_formater_class)
        parser.add_argument(
            "directory", type=pathlib.Path, help="project directory on remote"
        )
        parser.add_argument(
            "--config",
            type=str,
            default=get_active_config(),
            help="deployment configuration",
        )
        dev_open(parser.parse_args(rest))


if __name__ == "__main__":
    dev()
