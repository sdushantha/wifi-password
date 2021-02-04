#!/usr/bin/env python3
#
# by Siddharth Dushantha
#
import pathlib
import sys
import argparse
from shutil import which
import re
import os

import utils
import constants

__version__ = "1.0.7"

def print_error(text):
    print(f"ERROR: {text}", file=sys.stderr)
    sys.exit(1)

def get_ssid():
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

def main():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]')
    parser.add_argument('--qrcode', "-q", action="store_true", default=False, help="Generate a QR code")
    parser.add_argument('--image', "-i", action="store_true", default=False, help="Create the QR code as image instead of showing it on the terminal (must be used along with --qrcode)")
    parser.add_argument('--ssid', "-s", nargs='?', type=str, help="Specify a SSID that you have previously connected to")
    parser.add_argument('--list', "-l", action="store_true", default=False, help="Lists all stored network SSID")
    parser.add_argument('--version', action="store_true", help="Show version number")
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit()

    wifi_dict = {}

    if args.list:
        ssid = utils.get_ssid_list()
        wifi_dict= utils.generate_wifi_dict(ssid)
        utils.print_dict(wifi_dict)
        return

    ssid = get_ssid() if not args.ssid else args.ssid.split(',')

    if ssid:
        wifi_dict = utils.generate_wifi_dict(ssid)

    if args.qrcode:
        args.no_password = True

        for key, value in wifi_dict.items():
            utils.generate_qr_code(key, value, image=args.image)
        
        return

    utils.print_dict(wifi_dict)

if __name__ == "__main__":
    main()