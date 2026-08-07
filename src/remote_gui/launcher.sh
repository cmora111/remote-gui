#!/usr/bin/env bash

set -euo pipefail

RUNDIR=$(mktemp -d /tmp/remote-gui-runtime-XXXXXX)
chmod 700 "$RUNDIR"

cleanup() {
    rm -rf "$RUNDIR"
}

trap cleanup EXIT

env \
    XDG_RUNTIME_DIR="$RUNDIR" \
    GIO_USE_VFS=local \
    GTK_USE_PORTAL=0 \
    NO_AT_BRIDGE=1 \
    GTK_A11Y=none \
    SESSION_MANAGER= \
    dbus-run-session -- "$@"
