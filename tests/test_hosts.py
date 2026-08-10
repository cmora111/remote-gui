from remote_gui.hosts import parse_hosts


def test_parse_hosts():
    config = """
Host alienware
    HostName 192.168.1.100

Host spectrix
    HostName 192.168.1.101

Host *
    ForwardAgent yes
"""

    assert parse_hosts(config) == [
        "alienware",
        "spectrix",
    ]
