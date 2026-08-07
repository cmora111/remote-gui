import shlex
import subprocess
from importlib.resources import files


def launch(host: str, command: list[str], debug: bool = False) -> int:
    launcher = files("remote_gui").joinpath("launcher.sh")
    remote_command = "bash -s -- " + shlex.join(command)

    ssh_command = [
        "ssh",
        "-Y",
    ]

    if debug:
        ssh_command.append("-vv")

    ssh_command.extend([
        host,
        remote_command,
    ])

    if debug:
        print("SSH command:")
        print(shlex.join(ssh_command))

    try:
        with launcher.open("rb") as script:
            result = subprocess.run(
                ssh_command,
                stdin=script,
            )

        return result.returncode

    except FileNotFoundError:
        print("Error: ssh was not found.")
        return 127

    except KeyboardInterrupt:
        print("\nInterrupted.")
        return 130
