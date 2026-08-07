#!/usr/bin/env python3

import argparse
import shlex
import subprocess


REMOTE_ENV = r'''
RUNDIR=$(mktemp -d /tmp/remote-gui-runtime-XXXXXX)
chmod 700 "$RUNDIR"

cleanup() {{
    rm -rf "$RUNDIR"
}}

trap cleanup EXIT

env \
    XDG_RUNTIME_DIR="$RUNDIR" \
    GIO_USE_VFS=local \
    GTK_USE_PORTAL=0 \
    NO_AT_BRIDGE=1 \
    GTK_A11Y=none \
    SESSION_MANAGER= \
    dbus-run-session -- {command}
'''


def launch(host: str, command: list[str]) -> int:
    command_string = shlex.join(command)
    remote_script = REMOTE_ENV.format(command=command_string)

    ssh_command = [
        "ssh",
        "-Y",
        host,
        remote_script,
    ]

    return subprocess.call(ssh_command)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Launch remote Linux GUI applications over SSH/X11."
    )

    parser.add_argument(
        "host",
        help="SSH host alias, such as spectrix or alienware",
    )

    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Application and arguments to run remotely",
    )

    args = parser.parse_args()

    if not args.command:
        parser.error("You must specify an application to run.")

    return launch(args.host, args.command)


if __name__ == "__main__":
    raise SystemExit(main())
