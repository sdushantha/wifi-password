<h1 align="center">
wifi-password
</h1>
<p align="center">
Quickly fetch your WiFi password and if needed, generate a QR code of your WiFi to allow phones to easily connect.
<br>
Works on <b>macOS</b> and <b>Linux</b>, <b>Windows</b>
<img src="images/demo.gif" align="center">
</p>

## Installation

### Install using `pip`
```console
$ python3 -m pip install --user wifi-password
```

### Install using `git`
```
$ git clone https://github.com/sdushantha/wifi-password
$ cd wifi-password
$ python3 setup.py install
```

### Install using the [AUR](https://aur.archlinux.org/packages/wifi-password/)
- With `pamac`
```console
$ sudo pamac build wifi-password
```
- With `yay`
```console
$ yay -S wifi-password
```

---
---
## Usage
```console
$ wifi-password --help
usage: wifi_password [options]

optional arguments:
  -h, --help            show this help message and exit
  --show-qr, -show      Show a ASCII QR code onto the terminal/console
  --save-qr [PATH], -save [PATH]
                        Create the QR code and save it as an image
  --ssid SSID, -s SSID  Specify a SSID that you have previously connected to
  --list, -l            Lists all stored network SSID
  --version             Show version number
```

---
---
## Problems? Check this list
- ### Password not found:
  - **Linux:**
    - Make sure your network passwords are stored correctly in NetworkManager's storage directory. This is in /etc/NetworkManager/system-connections/. NetworkManager can work by checking if the passwords are stored with another program, but you need to store them in this directory for this program to work.
  - **MacOS/Windows:**
    - You probably have something broken with your WiFi storage. If not, submit an issue to this repository with information.
---
- ### NetworkManager isn't installed:
  - This program ***does not work*** without NetworkManager on Linux. If you want to use this program, install it using your distributions package manager or software center. Not using NetworkManager is a strange decision, but that's an issue for another time.
---
- ### Have another issue?
  - Open a useful issue on this GitHub, and/or suggest a new item in this list if you find a solution.

---
---
## Reference
- This project is an improvement of [wifi-password](https://github.com/rauchg/wifi-password) created by [@rauchg](https://github.com/rauchg), where I have added support for multiple platforms and have added the feature for generating QR codes.
- [wifiPassword](https://github.com/ankitjain28may/wifiPassword) created by [@ankitjain28may](https://github.com/ankitjain28may) was frequently used as reference throughout the development of this project.
