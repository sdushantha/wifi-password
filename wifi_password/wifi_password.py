#!/usr/bin/env python3

"""
Quickly fetch your WiFi password and if needed, generate a QR code
of your WiFi to allow phones to easily connect

by Siddharth Dushantha
"""

import pathlib
import sys
import subprocess
import argparse
from shutil import which
import re
import os
import qrcode
import colorama

__version__ = "1.1.1"


def run_command(command: str) -> str:
    """
    Runs a given command using subprocess module
    """
    env = os.environ.copy()
    env["LANG"] = "C"
    output, _ = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True, env=env).communicate()
    return output.decode("utf-8").rstrip("\r\n")


def print_error(text) -> None:
    """
    Shows an error message and exits the program with the status code 1
    """
    print(f"ERROR: {text}", file=sys.stderr)
    sys.exit(1)


def get_ssid() -> str:
    """
    Get the SSID which the computer is currently connected to
    """

    if sys.platform == "darwin":
        airport = pathlib.Path("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport")
        if not airport.is_file():
            print_error(f"Can't find 'airport' command at {airport}")

        ssid = run_command(f"{airport} -I | awk '/ SSID/ {{print substr($0, index($0, $2))}}'")

    elif sys.platform == "linux":
        if which("nmcli") is None:
            print_error("Network Manager is required to run this program on Linux.")

        ssid = run_command("nmcli -t -f active,ssid dev wifi | egrep '^yes:' | sed 's/^yes://'")

    elif sys.platform == "win32":
        ssid = run_command("netsh wlan show interfaces | findstr SSID")
        if ssid == "":
            print_error("SSID was not found")

        ssid = re.findall(r"[^B]SSID\s+:\s(.*)", ssid)[0]

    return ssid


def get_password(ssid: str) -> str:
    """
    Gets the password for a given SSID
    """

    if ssid == "":
        print_error("SSID is not defined")

    if sys.platform == "darwin":
        password = run_command(f"security find-generic-password -l \"{ssid}\" -D 'AirPort network password' -w")

    elif sys.platform == "linux":
        # Check if the user is running with super user privilages
        if os.geteuid() != 0:
            password = run_command(f"sudo nmcli -s -g 802-11-wireless-security.psk connection show '{ssid}'")
        else:
            password = run_command(f"nmcli -s -g 802-11-wireless-security.psk connection show '{ssid}'")

    elif sys.platform == "win32":
        password = run_command(f"netsh wlan show profile name=\"{ssid}\" key=clear | findstr Key")
        password = re.findall(r"Key Content\s+:\s(.*)", password)[0]

    if password == "":
        print_error("Could not find password")

    return password


def generate_qr_code(ssid: str, password: str, path: str, show_qr: bool) -> None:
    """
    Generate a QR code based on the given SSID and password
    """

    # Source: https://git.io/JtLIv
    text = f"WIFI:T:WPA;S:{ssid};P:{password};;"

    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10,
                       border=4)
    qr.add_data(text)

    if show_qr:
        # This will emulate support for ANSI escape sequences, which is needed
        # in order to display the QR code on Windows
        colorama.init()
        qr.make()
        qr.print_tty()

    if path:
        file_name = ssid.replace(" ", "_") + ".png"

        if path == "STORE_LOCALLY":
            path = file_name

        try:
            img = qr.make_image()
            img.save(path)
        except FileNotFoundError:
            print_error(f"No such file/directory: '{path}'")

        print(f"QR code has been saved to {path}")


def main() -> None:
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument("--show-qr", "-show",
                        action="store_true",
                        default=False,
                        help="Show a ASCII QR code onto the terminal/console")

    parser.add_argument("--save-qr", "-save",
                        metavar="PATH",
                        nargs="?",
                        const="STORE_LOCALLY",
                        help="Create the QR code and save it as an image")

    parser.add_argument("--ssid", "-s",
                        help="Specify a SSID that you have previously connected to")

    parser.add_argument("--version",
                        action="store_true",
                        help="Show version number")
    
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit()

    if args.ssid is None:
        args.ssid = get_ssid()

    password = get_password(args.ssid)

    if args.show_qr or args.save_qr:
        generate_qr_code(ssid=args.ssid, password=password, path=args.save_qr, show_qr=args.show_qr)
        return

    print(password)


if __name__ == "__main__":
    main()
