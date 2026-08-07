#!/usr/bin/env python3

import argparse

from remote_gui.ssh import launch
from remote_gui.ssh import launch, run_remote


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="remote-gui",
        description="Launch remote GUI applications over SSH/X11.",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show SSH debugging information.",
    )

    parser.add_argument(
        "host",
        help="SSH host alias, for example: spectrix or alienware",
    )

    parser.add_argument(
        "command",
        nargs=argparse.REMAINDER,
        help="Application and arguments to run remotely.",
    )

    return parser

def doctor_main() -> int:
    parser = argparse.ArgumentParser(
        prog="remote-gui-doctor",
        description="Check whether a remote host is ready for remote GUI apps.",
    )

    parser.add_argument("host", help="SSH host alias")

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show SSH debugging information.",
    )

    args = parser.parse_args()

    script = r'''
FAILED=0

pass_check() {
    printf "PASS  %s\n" "$1"
}

fail_check() {
    printf "FAIL  %s\n" "$1"
    FAILED=1
}

if [ -n "${DISPLAY:-}" ]; then
    pass_check "DISPLAY=$DISPLAY"
else
    fail_check "DISPLAY is not set"
fi

for cmd in xauth dbus-run-session bash mktemp; do
    if command -v "$cmd" >/dev/null 2>&1; then
        pass_check "$cmd installed"
    else
        fail_check "$cmd missing"
    fi
done

exit "$FAILED"
'''

    return run_remote(
        host=args.host,
        command=["bash", "-c", script],
        debug=args.debug,
    )

def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if not args.command:
        parser.error("You must specify an application to run.")

    return launch(
        host=args.host,
        command=args.command,
        debug=args.debug,
    )


def tilix_main() -> int:
    parser = argparse.ArgumentParser(
        prog="remote-tilix",
        description="Launch Tilix remotely over SSH/X11.",
    )

    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show SSH debugging information.",
    )

    parser.add_argument(
        "host",
        help="SSH host alias, for example: spectrix or alienware",
    )

    args = parser.parse_args()

    return launch(
        host=args.host,
        command=["tilix", "--new-process"],
        debug=args.debug,
    )


if __name__ == "__main__":
    raise SystemExit(main())
