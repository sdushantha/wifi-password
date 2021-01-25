<h1 align="center">
wifi-password
</h1>
<p align="center">
Generate a QR code of your WiFi allowing other devices to easily connect without having to type the password
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
