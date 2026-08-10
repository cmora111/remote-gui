from pathlib import Path


def parse_hosts(config_text: str) -> list[str]:
     """Return explicit host aliases from an OpenSSH configuration."""

    hosts: set[str] = set()

    for line in config_text.splitlines():
        line = line.strip()

        if not line or line.startswith("#"):
            continue

        parts = line.split()

        if not parts or parts[0].lower() != "host":
            continue

        for host in parts[1:]:
            if "*" in host or "?" in host or host.startswith("!"):
                continue

            hosts.add(host)

    return sorted(hosts)


def hosts_command(args) -> int:
    config_path = Path.home() / ".ssh" / "config"

    if not config_path.exists():
        print(f"No SSH config found at {config_path}")
        return 1

    config_text = config_path.read_text(encoding="utf-8")
    hosts = parse_hosts(config_text)

    if not hosts:
        print("No explicit SSH host aliases found.")
        return 0

    print("Configured SSH hosts:")

    for host in hosts:
        print(f"  {host}")

    return 0
