import sys
import argparse

from img_upload_backend import __version__


def cli() -> str:
    """This Function is repsonsible for the command line interface.

    Returns:
        str: Path to the config File
    """
    parser = argparse.ArgumentParser(
        prog="img_upload_backend",
        description="This will start the image uplaod backend",
    )
    parser.add_argument(
        "--config",
        "-c",
        help="path to the configuration file",
        default="./config.toml",
        type=str,
    )
    parser.add_argument(
        "--version", "-v", help="print version and exit", action="store_true"
    )

    inputvars = parser.parse_args()

    if inputvars.version:
        print(__version__)
        sys.exit(0)

    print(f"""version: {__version__}"""
    )

    return inputvars.config
