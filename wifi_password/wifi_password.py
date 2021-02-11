#!/usr/bin/env python3
#
# by Siddharth Dushantha
#

import sys
import argparse
import re
import os

__version__ = "1.0.9"

def main():
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")
    parser.add_argument(
        "--qrcode", "-q", action="store_true", default=False, help="Generate a QR code"
    )
    parser.add_argument(
        "--image",
        "-i",
        action="store_true",
        default=False,
        help="Create the QR code as image instead of showing it on the terminal (must be used along with --qrcode)",
    )
    parser.add_argument(
        "--ssid", "-s", help="Specify a SSID that you have previously connected to"
    )
    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        default=False,
        help="Lists all stored network SSID",
    )
    parser.add_argument("--version", action="store_true", help="Show version number")
    args = parser.parse_args()

    if args.version:
        print(__version__)
        sys.exit()

    wifi_dict = {}

    if args.list:
        profiles = utils.get_profiles()
        wifi_dict = utils.generate_wifi_dict(profiles)
        utils.print_dict(wifi_dict)
        return

    if args.ssid is None:
        args.ssid = utils.get_ssid()

    ssid = utils.get_ssid() if not args.ssid else args.ssid.split(",")

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
