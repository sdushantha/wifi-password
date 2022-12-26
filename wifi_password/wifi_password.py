#!/usr/bin/env python3

"""
Quickly fetch your WiFi password and if needed, generate a QR code
of your WiFi to allow phones to easily connect

by Siddharth Dushantha
"""

import pathlib
import sys
import argparse
from shutil import which
import re
import os

import utils
import constants

__version__ = "1.1.1"

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
    platform = utils.get_platform()

    if platform == constants.MAC:
        airport = pathlib.Path(constants.AIRPORT_PATH)

        if not airport.is_file():
            print_error(f"Can't find 'airport' command at {airport}")
        
        ssid = utils.run_command(f"{airport} -I | awk '/ SSID/ {{print substr($0, index($0, $2))}}'")

    elif platform == constants.LINUX:
        if which("nmcli") is None:
            print_error("Network Manager is required to run this program on Linux.")

        ssid = utils.run_command("nmcli -t -f active,ssid dev wifi | egrep '^yes:' | sed 's/^yes://'")

    elif platform == constants.WINDOWS:
        ssid = utils.run_command("netsh wlan show interfaces | findstr SSID")

        if ssid == "":
            print_error("SSID was not found")

        ssid = re.findall(r"[^B]SSID\s+:\s(.*)", ssid)[0]

    return ssid

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

    parser.add_argument('--list', "-l", 
                        action="store_true", 
                        default=False, 
                        help="Lists all stored network SSID")

    parser.add_argument("--version",
                        action="store_true",
                        help="Show version number")
    
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit()

    wifi_dict = {}

    if args.list:
        profiles = utils.get_profiles()
        wifi_dict= utils.generate_wifi_dict(profiles)
        utils.print_dict(wifi_dict)
        return

    if args.ssid is None:
        args.ssid = get_ssid()

    ssid = get_ssid() if not args.ssid else args.ssid.split(',')

    if ssid:
        wifi_dict = utils.generate_wifi_dict(ssid)

    if args.show_qr or args.save_qr:
        for key, value in wifi_dict.items():
            utils.generate_qr_code(ssid=key, password=value, path=args.save_qr, show_qr=args.show_qr)
        return

    utils.print_dict(wifi_dict)

if __name__ == "__main__":
    main()