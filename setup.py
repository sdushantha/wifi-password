import setuptools

with open("README.md", 'r', encoding="utf-8") as f:
    long_description = f.read()

setuptools.setup(
    name='wifi-password',
    version='1.0.1',
    author='Siddharth Dushantha',
    author_email='siddharth.dushantha@gmail.com',
    description='Quickly fetch your WiFi password and if needed, generate a QR code of your WiFi to allow phones to easily connect',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/sdushantha/wifi-password',
    packages=setuptools.find_packages(),
    entry_points={'console_scripts': ['wifi-password = wifi_password.wifi_password:main']},
    install_requires=['qrcode'],
)
