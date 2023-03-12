from argparse import Namespace

from devproject.utils import get_config, save_config


def config(args: Namespace) -> None:
    try:
        config = get_config()
    except FileNotFoundError:
        config = {}
    if args.rm:
        config.pop(args.name)
        for i, k in enumerate(config):
            config[k]["active"] = "True" if i == 0 else "False"
    else:
        if args.name not in config:
            assert args.deployment_path
            config[args.name] = {
                "name": args.name,
                "deployment_path": str(args.deployment_path),
                "gateway": args.gateway,
                "host": "sync" if args.sync_host else args.gateway,
                "active": "True",
            }
        for k in config:
            config[k]["active"] = "True" if k == args.name else "False"
    save_config(config)
