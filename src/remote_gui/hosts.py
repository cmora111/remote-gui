from pathlib import Path


def hosts_command(args) -> int:
    config_path = Path.home() / ".ssh" / "config"

    if not config_path.exists():
        print(f"No SSH config found at {config_path}")
        return 1

    hosts: set[str] = set()

    with config_path.open("r", encoding="utf-8") as config:
        for line in config:
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

    if not hosts:
        print("No explicit SSH host aliases found.")
        return 0

    print("Configured SSH hosts:\n")

    for host in sorted(hosts):
        print(f"  {host}")

    return 0
