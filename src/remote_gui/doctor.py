from remote_gui.ssh import run_remote


def doctor_command(args) -> int:
    """Run diagnostic checks against a remote host."""

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
        dry_run=args.dry_run,
    )
