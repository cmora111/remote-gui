from remote_gui.ssh import build_ssh_command


def test_build_ssh_command():
    cmd = build_ssh_command(
        host="spectrix",
        command=["xclock"],
    )

    assert cmd == [
        "ssh",
        "-Y",
        "spectrix",
        "bash -s -- xclock",
    ]


def test_build_ssh_command_debug():
    cmd = build_ssh_command(
        host="spectrix",
        command=["xclock"],
        debug=True,
    )

    assert cmd == [
        "ssh",
        "-Y",
        "-vv",
        "spectrix",
        "bash -s -- xclock",
    ]

def test_build_ssh_command_with_arguments():
    cmd = build_ssh_command(
        host="spectrix",
        command=["gedit", "--new-window", "notes.txt"],
    )

    assert cmd == [
        "ssh",
        "-Y",
        "spectrix",
        "bash -s -- gedit --new-window notes.txt",
    ]
