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

def get_windows_profiles():
    """
    Gets a list of names from saved wifi networks in Windows

    Reference: https://www.geeksforgeeks.org/getting-saved-wifi-passwords-using-python/
    """
    profiles = []

    try:
        # getting meta data
        meta_data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles'])

        # decoding meta data and splitting data line by line
        data = meta_data.decode('utf-8', errors='backslashreplace')
        data = data.split('\n')

        # get meta data for profile names
        profiles = [d.split(':')[1][1:-1] for d in data if "All User Profile" in d]
    except subprocess.CalledProcessError:
        pass

    return profiles

def get_linux_profiles():
    """
    Gets a list of names from saved wifi networks in Linux
    """
    profiles = []

    try:
        pass
    except:
        pass

    return profiles

def get_mac_profiles():
    """
    Gets a list of names from saved wifi networks in MacOS
    """
    profiles = []

    try:
        pass
    except:
        pass

    return profiles

def get_ssid_list():
    """
    Returns a list of SSIDs
    """
    ssid = []

    platform = get_platform()

    if platform == constants.MAC:
        ssid = get_mac_profiles()
    elif platform == constants.LINUX:
        ssid = get_linux_profiles()
    elif platform == constants.WINDOWS:
        ssid = get_windows_profiles()

    return ssid

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
            password = password.replace("\n", "")
        elif platform == constants.LINUX:
            # Check if the user is running with super user privilages
            if os.geteuid() != 0:
                print(f"You need to run the application as root")
            else:
                password = run_command(f"cat /etc/NetworkManager/system-connections/{ssid}.nmconnection | grep psk=")
                password = password.replace("\n", "")
                password = password[4:]
        elif platform == constants.WINDOWS:
            password = run_command(f"netsh wlan show profile name=\"{ssid}\" key=clear | findstr Key").replace("\r", "")

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
    return output.decode("utf-8")

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
