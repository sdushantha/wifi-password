#!/usr/bin/env python3

"""
Quickly fetch your WiFi password and if needed, generate a QR code
of your WiFi to allow phones to easily connect

by Siddharth Dushantha

Feature List:

version 1.1.2
    - Added fixes from the commit from [GoDoVoReZ:feature](https://github.com/GoDoVoReZ/wifi-password/tree/feature)
    - Added support for the Russian language of the system interface and cp866 encoding
    - Added the ability to display SSID and password in terminal/console
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

__version__ = "1.1.2"

colorama.init(autoreset=True)

def run_command(command: str) -> str:
    """
    Runs a given command using subprocess module
    """
    env = os.environ.copy()
    env["LANG"] = "C"
    raw_output, _ = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True, env=env).communicate()
    
    try:
        output = raw_output.decode("utf-8").strip("\r\n")
    except UnicodeDecodeError:
        # For windows 7
        output = raw_output.decode("cp866").strip("\r\n")

    return output


def print_error(text) -> None:
    """
    Shows an error message and exits the program with the status code 1
    """
    print(colorama.Fore.RED + f"ERROR: {text}", file=sys.stderr)
    sys.exit(1)


def print_info(text) -> None:
    """
    Shows an info message
    """
    print(colorama.Fore.MAGENTA + f"INFO: {text}", file=sys.stdout)


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
        output = run_command("netsh wlan show interfaces | findstr SSID")
        if output == "":
            print_error("error getting SSID")

        result = re.findall(r"[^B]SSID\s+:\s(.*)", output)

        if len(result) > 0:
            ssid = result[0]
        else:
            ssid = ""

    if ssid == "":
        print_error("Could not find SSID")

    return ssid.replace("\r", "")


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
        if os.getuid() != 0:
            password = run_command(f"sudo nmcli -s -g 802-11-wireless-security.psk connection show '{ssid}'")
        else:
            password = run_command(f"nmcli -s -g 802-11-wireless-security.psk connection show '{ssid}'")

    elif sys.platform == "win32":
        output = run_command(f"netsh wlan show profile name=\"{ssid}\" key=clear")
        # 
        result = re.findall(r"Key Content\s+:\s(.*)", output)
        # if system language russian
        if result == []:
            result = re.findall(r"Содержимое ключа\s+:\s(.*)", output)

        if len(result) > 0:
            password = result[0]
        else:
            password = ""

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
        print_info('QR CODE:')
        qr.print_tty()

    if path:
        file_name = ssid.replace(" ", "_")
        file_name = file_name.replace(".", "_")

        if path == "STORE_LOCALLY":
            path = file_name + ".png"

        try:
            img = qr.make_image()
            img.save(path)
        except FileNotFoundError:
            print_error(f"No such file/directory: {path}")

        print_info(f"QR code has been saved to: {path}")


def main() -> None:
    parser = argparse.ArgumentParser(usage="%(prog)s [options]")

    parser.add_argument("--show-txt", "-text",
                        action="store_true",
                        default=False,
                        help="Show a ASCII ssid and password code onto the terminal/console")

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
        print_info(__version__)
        sys.exit(0)

    if args.ssid is None:
        args.ssid = get_ssid()

    password = get_password(args.ssid)

    if args.show_qr or args.save_qr:
        generate_qr_code(ssid=args.ssid, password=password, path=args.save_qr, show_qr=args.show_qr)

    elif args.show_txt:
        print_info(f'SSID: {args.ssid}\tPASSWORD: {password}')
  
    else:
        print_info(f'SSID: {args.ssid}\tPASSWORD: {password}')  
    
    return 0


if __name__ == "__main__":
    main()
