#!/usr/bin/env python3
import os
import sys
import re
import subprocess
import qrcode

import constants

def get_platform():
    """
    Returns the name of the platform where the application is currently running
    """
    platforms = {
        'linux1': constants.LINUX,
        'linux2': constants.LINUX,
        'darwin': constants.MAC,
        'win32': constants.WINDOWS
    }

    if not sys.platform in platforms:
        return sys.platform

    return platforms[sys.platform]

def get_profiles():
    """
    Gets a list of names from saved wifi networks in the current platform
    """
    profiles = []

    platform = get_platform()

    try:
        if platform == constants.MAC:
            pass
        elif platform == constants.LINUX:
            pass
        elif platform == constants.WINDOWS:
            # Reference: https://www.geeksforgeeks.org/getting-saved-wifi-passwords-using-python/
            # getting meta data
            meta_data = run_command('netsh wlan show profiles | findstr ":"')

            if meta_data != "":
                # splitting data line by line
                data = meta_data.split('\n')

                if len(data) > 0:
                    # skip the first element in data since it does not contain a valid profile returned by netsh command
                    profiles = [d.split(':')[1].strip(' .\r') for d in data[1:]]
    except Exception as ex:
        print(f'Error: {ex}')

    return profiles

def generate_wifi_dict(profiles: list):
    """
    Generates a dictionary with the wifi name as key and the password as it's value
    """
    wifi_dict = {}

    if profiles is None:
        print(f'List is not defined.')
        return

    if len(profiles) == 0:
        print(f'List is empty.')
        return

    for ssid in profiles:
        password = get_password(ssid)

        wifi_dict[ssid] = password

    return wifi_dict

def get_password(ssid: str):
    """
    Gets the password for a given SSID
    """
    password = ""

    if ssid == "" or ssid is None:
        print("SSID is not defined")
        return password

    platform = get_platform()

    try:
        if platform == constants.MAC:
            password = run_command(f"security find-generic-password -l \"{ssid}\" -D 'AirPort network password' -w")
        elif platform == constants.LINUX:
            # Check if the user is running with super user privilages
            if os.geteuid() != 0:
                password = run_command(f"sudo nmcli -s -g 802-11-wireless-security.psk connection show '{ssid}'")
            else:
                password = run_command(f"nmcli -s -g 802-11-wireless-security.psk connection show '{ssid}'")
        elif platform == constants.WINDOWS:
            password = run_command(f"netsh wlan show profile name=\"{ssid}\" key=clear | findstr Key")

            if password != "":
                password = re.findall(r"Key Content\s+:\s(.*)", password)[0]
    except Exception as ex:
        print(f'Error: {ex}')

    return password

def run_command(command: str):
    """
    Runs a given command using subprocess module
    """
    if command == "" or command is None:
        return ""
    
    output, _ = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, shell=True).communicate()
    return output.decode("utf-8", errors="replace").rstrip('\r\n')

def print_dict(ssid: dict):
    """
    Prints the contents of the given dictionary that contains the wifi name and password
    """
    if ssid is None:
        print(f'Dictionary is not defined.')
        return

    if len(ssid) == 0:
        print(f'Dictionary is empty.')
        return

    print("----------------------------------------------")
    print("{:<30}| {:<}".format("SSID", "Password"))
    print("----------------------------------------------")

    for key, value in ssid.items():
        print("{:<30}| {:<}".format(key, value))

    print("----------------------------------------------")

def generate_qr_code(ssid: str, password: str, image: bool = False):
    """
    Generates a QR code from a given ssid and password

    Source: https://git.io/JtLIv
    """
    if ssid == "" or ssid is None:
        print('SSID is not specified, cannot generate QR code.')
        return

    text = f"WIFI:T:WPA;S:{ssid};P:{password};;"

    try:
        qr = qrcode.QRCode(version=1,
                        error_correction=qrcode.constants.ERROR_CORRECT_L,
                        box_size=10,
                        border=4)
        qr.add_data(text)

        if image:
            file_name = ssid.replace(" ", "_") + ".png"
            img = qr.make_image()
            img.save(file_name)
            print(f"QR code has been saved to '{file_name}'.")
        else:
            qr.make()
            qr.print_tty()
    except Exception as ex:
        print(f'QR Code Error: {ex}')
