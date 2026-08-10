#!/usr/bin/env python3

import argparse
from pathlib import Path
from remote_gui.ssh import launch, run_remote
from remote_gui.doctor import doctor_command
from remote_gui.hosts import hosts_command
from remote_gui.version import get_version


def add_common_options(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show SSH debugging information.",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be executed without running it.",
    )


def run_command(args: argparse.Namespace) -> int:
    if not args.command:
        raise SystemExit("You must specify an application to run.")

    return launch(
        host=args.host,
        command=args.command,
        debug=args.debug,
        dry_run=args.dry_run,
    )

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="remote-gui",
        description="Launch remote GUI applications over SSH/X11.",
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}",
    )

    subparsers = parser.add_subparsers(
        dest="subcommand",
        required=True,
    )

    run_parser = subparsers.add_parser(
        "run",
        help="Launch a remote GUI application.",
    )

    add_common_options(run_parser)

    run_parser.add_argument(
        "host",
        help="SSH host alias, for example: spectrix or alienware",
    )

    run_parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Application and arguments to run remotely.",
    )

    run_parser.set_defaults(func=run_command)

    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Check whether a remote host is ready for GUI forwarding.",
    )

    hosts_parser = subparsers.add_parser(
        "hosts",
        help="List host aliases from ~/.ssh/config.",
    )

    hosts_parser.set_defaults(func=hosts_command)

    add_common_options(doctor_parser)

    doctor_parser.add_argument(
        "host",
        help="SSH host alias to test.",
    )

    doctor_parser.set_defaults(func=doctor_command)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    return args.func(args)


def tilix_main() -> int:
    parser = argparse.ArgumentParser(
        prog="remote-tilix",
        description="Launch Tilix remotely over SSH/X11.",
    )

    add_common_options(parser)

    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {get_version()}",
    )

    parser.add_argument(
        "host",
        help="SSH host alias.",
    )

    args = parser.parse_args()

    return launch(
        host=args.host,
        command=["tilix", "--new-process"],
        debug=args.debug,
        dry_run=args.dry_run,
    )


if __name__ == "__main__":
    raise SystemExit(main())
