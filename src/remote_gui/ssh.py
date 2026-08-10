import shlex
import subprocess
from importlib.resources import files

def get_launcher():
    return files("remote_gui").joinpath("launcher.sh")


def build_ssh_command(
    host: str,
    command: list[str],
    debug: bool = False,
) -> list[str]:
    remote_command = "bash -s -- " + shlex.join(command)

    ssh_command = ["ssh", "-Y"]

    if debug:
        ssh_command.append("-vv")

    ssh_command.extend([
        host,
        remote_command,
    ])

    return ssh_command


def run_remote(
    host: str,
    command: list[str],
    debug: bool = False,
    dry_run: bool = False,
) -> int:
    ssh_command = ["ssh", "-Y"]

    if debug:
        ssh_command.append("-vv")

    ssh_command.extend([
        host,
        shlex.join(command),
    ])

    if debug or dry_run:
        print(shlex.join(ssh_command))

    if dry_run:
        return 0

    try:
        return subprocess.run(ssh_command).returncode
    except FileNotFoundError:
        print("Error: ssh command was not found.")
        return 127
    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130

def print_dry_run(host: str, command: list[str], ssh_command: list[str], launcher) -> None:
    print(f"Remote host : {host}")
    print(f"Application : {shlex.join(command)}")
    print(f"Launcher    : {launcher}\n")
    print("Equivalent command:\n")
    print(
        f"{shlex.join(ssh_command)} \\\n"
        f"    < {shlex.quote(str(launcher))}"
    )


def launch(
    host: str,
    command: list[str],
    debug: bool = False,
    dry_run: bool = False,
) -> int:
    launcher = get_launcher()
    ssh_command = build_ssh_command(host, command, debug)

    if dry_run:
        print_dry_run(host, command, ssh_command, launcher)
        return 0

#    if dry_run:
#        print(f"Remote host : {host}")
#        print(f"Application : {shlex.join(command)}")
#        print(f"Launcher    : {launcher}")
#        print()
#        print("Equivalent command:")
#        print()
#        print(
#            f"{shlex.join(ssh_command)} \\\n"
#            f"    < {shlex.quote(str(launcher))}"
#        )
#        return 0

    if debug:
        print("SSH command:")
        print(shlex.join(ssh_command))

    try:
        with launcher.open("rb") as script:
            return subprocess.run(
                ssh_command,
                stdin=script,
            ).returncode

    except FileNotFoundError:
        print("Error: ssh command was not found.")
        return 127

    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130
