from remote_gui.hosts import parse_hosts


def test_parse_hosts_ignores_wildcards_and_comments():
    config = """
# Sample config

Host *
    ForwardAgent yes

Host !internal
    User mora

Host alienware spectrix
    User mora

Host r400?
    User mora
"""

    assert parse_hosts(config) == [
        "alienware",
        "spectrix",
    ]
