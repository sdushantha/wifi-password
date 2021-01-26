<h1 align="center">
wifi-password
</h1>
<p align="center">
Quickly fetch your WiFi password and if needed, generate a QR code of your WiFi to allow phones to easily connect.
<br>
Works on macOS and Linux and Windows.
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

## Usage
```console
$ wifi-password
usage: wifi-password [options]

optional arguments:
  -h, --help            show this help message and exit
  --qrcode, -q          Don't generate a QR code
  --image, -i           Create QR code as image instead of showing it on the terminal
  --ssid SSID, -s SSID  Specify a SSID that you have previously connected to
  --version             Show version number
```

## Reference
- This project is a improvement of [wifi-password](https://github.com/rauchg/wifi-password) created by [@rauchg](https://github.com/rauchg), where I have added support for mutliple platforms and have added the feature for generating QR codes.
- [wifiPassword](https://github.com/ankitjain28may/wifiPassword) created by [@ankitjain28may](https://github.com/ankitjain28may) was frequently used as referece throughout the development of this project.
