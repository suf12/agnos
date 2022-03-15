#!/usr/bin/env python3
__author__ = "Yusuf Hashmi <yusufjh@gmail.com>"
__date__ = "3/15/2022"
__version__ = "0.0.0"

import argparse
import ipaddress
import logging
import platform
import subprocess
import time
from pathlib import Path

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    "%(asctime)s - %(funcName)s:%(thread)d - %(levelname)s - %(message)s"
)

file_handler = logging.FileHandler("output.log")
stream_handler = logging.StreamHandler()

file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)
stream_handler.setLevel(logging.INFO)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)


class AgnOS(object):
    """OS Agnostic class. Saves logging details to script location under name output.log
    # API:
    write_file(path) Creates a text file containing 'Hello' at given full path.\n
    ping_addr(address) Pings the given IP address n times\n
    run_script() Runs test.(bat|sh) script from your PATH\n
    ## CONSTANTS
    TEXT_CONTENT\n
    SCRIPT_NAME\n
    NUM_PACKETS\n
    PING_ARG\n
    SCRIPT_EXT\n
    TIMEOUT\n
    """

    CLASS_CONSTANTS = {
        "TEXT_CONTENT": "Hello",
        "SCRIPT_NAME": "test",
        "NUM_PACKETS": 3,
        "TIMEOUT": 5,
    }

    SUPPORTED_OS = ["Windows", "Linux", "Darwin"]

    def __init__(self):
        """Parameters: None
        Determines the OS type and sets constants"""

        logger.debug(f"constants detected to be: {self.CLASS_CONSTANTS}")

        system = platform.system()
        if system in self.SUPPORTED_OS:
            if system == "Windows":
                self.PING_ARG = "-n"
                self.SCRIPT_EXT = "bat"
            elif system == "Linux":
                self.PING_ARG = "-c"
                self.SCRIPT_EXT = "sh"
            elif system == "Darwin":
                self.PING_ARG = "-c"
                self.SCRIPT_EXT = "sh"
        else:
            logger.critical(f"OS {system} is not supported. Exiting...")
            raise SystemExit(2)
        logger.info(f"OS detected to be {system}!")
        logger.debug(
            f"ping argument set to '{self.PING_ARG}', script extension set to '.{self.SCRIPT_EXT}'"
        )

    def timer(func):
        """A simple decorator for logging function execution time"""

        def wrapper(*args, **kwargs):
            logger.debug("starting the timer...")
            start = time.time()
            func(*args, **kwargs)
            total = time.time() - start
            logger.debug(f"{func.__name__} function completed in {total} seconds")

        return wrapper

    @timer
    def write_file(self, path="./", filename="hello"):
        """Parameters: filepath and filename, defaults to ./hello.txt
        Writes TEXT_CONTENT to the specified filepath/filename.txt"""

        # Set the absolute path of the text file
        filepath = path
        filename = filename
        SUFFIX = ".txt"
        full_path = Path(filepath, filename).with_suffix(SUFFIX).absolute()
        logger.debug(f"absolute path of file determined to be {full_path}")

        logger.info("writing the file...")
        try:
            with open(full_path, "w") as file:
                file.write(self.CLASS_CONSTANTS["TEXT_CONTENT"])
        except (PermissionError, FileNotFoundError) as e:
            logger.error(f"issue writing file: {e}")
        else:
            logger.info(f"file has been written at {full_path}!")

    @timer
    def ping_addr(self, address):
        """Parameters: IP Address
        Pings the specified address NUM_PACKETS times, timeout is after TIMEOUT seconds
        """
        try:
            # Check for valid IP address
            ipaddress.ip_address(address)
        except ValueError as e:
            logger.critical(f"{e}")
            return None
        else:
            logger.debug(f"{address} has a valid syntax")
        logger.info(f"attempting to ping {address}...")
        try:
            output = subprocess.run(
                [
                    "ping",
                    f"{self.PING_ARG}",
                    f"{self.CLASS_CONSTANTS['NUM_PACKETS']}",
                    f"{address}",
                ],
                timeout=self.CLASS_CONSTANTS["TIMEOUT"],
                capture_output=True,
                text=True,
            )
            logger.debug(f"ping output: {output.stdout}")
        except subprocess.TimeoutExpired as e:
            logger.error(f"{e}. {address} is unreachable!")
        else:
            logger.info(f"ping successful!")

    @timer
    def run_script(self):
        """Parameters: None
        Executes script named SCRIPT_NAME. Assumed to be defined in system PATH
        """
        try:
            logger.info(
                f"executing {self.CLASS_CONSTANTS['SCRIPT_NAME']}.{self.SCRIPT_EXT}..."
            )
            output = subprocess.run(
                [f"{self.CLASS_CONSTANTS['SCRIPT_NAME']}.{self.SCRIPT_EXT}"],
                timeout=self.CLASS_CONSTANTS["TIMEOUT"],
                capture_output=True,
                text=True,
            )
            logger.debug(f"script output: {output.stdout}")
        except (FileNotFoundError, subprocess.TimeoutExpired) as e:
            logger.error(f"issue running script: {e}")
        else:
            logger.info("successfully executed script!")


if __name__ == "__main__":
    """Parameters: IP Address and Filename
    Executes if program is invoked directly"""
    parser = argparse.ArgumentParser(
        description="This script is meant to demonstrate OS agnostic functionality",
        epilog=f"%(prog)s v{__version__} by {__author__}",
    )
    parser.add_argument(
        "-a", "--address", metavar="", required=True, help="IP address to ping"
    )
    parser.add_argument(
        "-p",
        "--path",
        metavar="",
        required=True,
        help="Path to generated text file",
    )
    parser.add_argument(
        "-f",
        "--file",
        metavar="",
        help="Name of the generated text file, defaults to hello",
        default="hello",
    )
    args = parser.parse_args()
    logger.debug(f"cli args detected to be {args}")

    command = AgnOS()
    command.write_file(args.path, args.file)
    command.ping_addr(args.address)
    command.run_script()
