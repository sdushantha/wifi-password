#!/usr/bin/env python3
#
# by Siddharth Dushantha
#
import pathlib
import sys
import subprocess
import argparse
from shutil import which
import re
import os
import qrcode

__version__ = "1.0.1"

def run_command(command):
    output, _ = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True).communicate()
    return output.decode("utf-8")


def print_error(text):
    print(f"ERROR: {text}")
    sys.exit(1)


def get_ssid():
    if sys.platform == "darwin":
        airport = pathlib.Path("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport")
        if not airport.is_file():
            print_error(f"Can't find 'airport' command at {airport}")

        ssid = run_command(f"{airport} -I | awk '/ SSID/ {{print substr($0, index($0, $2))}}'")
        ssid = ssid.replace("\n", "")

    elif sys.platform == "linux":
        if which("iwgetid") is not None:
            print_error("Can't find the 'iwgetid' command")
        
        ssid = run_command("iwgetid -r")
        ssid = ssid.replace("\n", "")

    elif sys.platform == "win32":
        ssid = run_command("netsh wlan show interfaces | findstr SSID").replace("\r", "")
        ssid = re.findall(r"[^B]SSID\s+:\s(.*)", ssid)[0]

    return ssid


def get_password(ssid):
    if sys.platform == "darwin":
        password = run_command(f"security find-generic-password -l \"{ssid}\" -D 'AirPort network password' -w")
        password = password.replace("\n", "")

    elif sys.platform == "linux":
        # Check if the user is running with super user privilages
        if os.geteuid() != 0:
            print_error(f"You need to run '{sys.argv[0]}' as root")

        password = run_command(f"cat /etc/NetworkManager/system-connections/{ssid} | grep psk=")
        password = password.replace("\n", "")

    elif sys.platform == "win32":
        password = run_command(f"netsh wlan show profile name=\"{ssid}\" key=clear | findstr Key").replace("\r", "")
        password = re.findall(r"Key Content\s+:\s(.*)", password)[0]

    if password == "":
        print_error("Cound not find password")

    return password


def generate_qr_code(ssid, password, image=False):
    # Source: https://git.io/JtLIv
    text = f"WIFI:T:WPA;S:{ssid};P:{password};;"

    qr = qrcode.QRCode(version=1,
                       error_correction=qrcode.constants.ERROR_CORRECT_L,
                       box_size=10,
                       border=4)
    qr.add_data(text)

    if image:
        file_name = ssid.replace(" ", "_") + ".png"
        img = qr.make_image()
        img.save(file_name)
        print(f"QR code has been saved to {file_name}")
    else:
        qr.make()
        qr.print_tty()


def main():
    parser = argparse.ArgumentParser(usage='%(prog)s [options]')
    parser.add_argument('--qrcode', "-q", action="store_true", default=False, help="Don't generate a QR code")
    parser.add_argument('--image', "-i", action="store_true", default=False, help="Create QR code as image instead of showing it on the terminal")
    parser.add_argument('--ssid', "-s", default=get_ssid(), help="Specify a SSID that you have previously connected to")
    parser.add_argument('--version', action="store_true", help="Show version number")
    args = parser.parse_args()

    if args.version:
        print(__version__)

    password = get_password(args.ssid)

    if args.qrcode:
        args.no_password = True
        generate_qr_code(args.ssid, password, image=args.image)
        return

    print(password)

if __name__ == "__main__":
    main()
