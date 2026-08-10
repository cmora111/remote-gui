from importlib.metadata import PackageNotFoundError, version


def get_version() -> str:
    """Return the installed package version."""

    try:
        return version("remote-gui")
    except PackageNotFoundError:
        return "development"
