from importlib.resources import files


def get_launcher_path():
    """Return the packaged launcher script."""
    return files("remote_gui").joinpath("launcher.sh")
