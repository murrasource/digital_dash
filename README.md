# digital_dash
A digital dashboard using Python, a Raspberry Pi Zero W, and vehicle's On Board Diagnostics (OBD-II) Port.

## Motivation
My personal reason for creating this was because my car's fuel sensor broke. The cost for repair was astronomical, so I figured creating a program to calculate the fuel level and milage would be much cheaper.

Really, though, this is easily made into just a fun digital dashboard for anyone who wants to experiment with 'carputers.'

## How It Works
The real guts of this operation is in the OBD-II port of pretty much every car since the 1996. OBD (On Board Diagnostics) lets you access the car's computer and retrieve information from it. Scroll down to see my supplies list.

Every tenth of a second, the program queries the OBD port for the data I want through the obd python library. Dependencies are also listed below.

## Hardware
1. Raspberry Pi Zero W (Note: if you use the display I chose, you will need the DPIO header pins on the Pi. It makes a very compact and easily mountable assembly.)
2. Touchscreen Display of your choice. I like the hyperpixel4 from Pimoroni. (https://shop.pimoroni.com/products/hyperpixel-4?variant=12569485443155)
3. Bluetooth ELM327 OBD-II Device (https://www.amazon.com/gp/product/B011NSX27A/ref=ppx_yo_dt_b_asin_title_o01_s00?ie=UTF8&psc=1)
4. OBD-II port splitter (https://www.amazon.com/gp/product/B0711LGRGQ/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)
5. OBD-II to micro USB power supply (https://www.amazon.com/gp/product/B074M4XMBX/ref=ppx_yo_dt_b_asin_title_o00_s00?ie=UTF8&psc=1)

## Dependencies
1. OBD `pip install obd`
2. PyQt5 `sudo apt-get install python3-pyqt5`
3. BlueZ Protocol `sudo apt-get install bluez`

## Hyperpixel4.0 Display Setup
Run these commands in the terminal
1. `curl -sSL https://get.pimoroni.com/hyperpixel4 | bash`
2. `hyperpixel4-rotate right`
3. `reboot`

## Bluetooth Setup
There have been some issues connecting the Raspberry Pi to ELM327 Devices. You might get the error `this device has no services which can be used with Raspberry Pi` when trying to connect the adapter. Here is how to successfully set it up.

1. Use the Bluetooth GUI or `bluetoothctl`
2. `sudo nano /etc/systemd/system/dbus-org.bluez.service`
3. Add/edit these lines
    ```
    ExecStart=/usr/lib/bluetooth/bluetoothd -C
    ExecStartPost=/usr/bin/sdptool add SP
    ```
4. `reboot`
5. `sudo rfcomm connect 0 <mac_address> 1` You can get the MAC Address by using `bluetoothctl`'s `devices` command.
Many thanks to this website for helping me out with this part: https://www.lukinotes.com/2018/10/raspberry-pi-bluetooth-connection.html

That should do the trick for setting up bluetooth. To double check, try opening python in the terminal, and run this:
```
from obd import *
connection = obd.OBD()
connection.status()
```
It will return a string telling you the status of the connection. Go here for more information: https://python-obd.readthedocs.io/en/latest/Connections/.

## Code Setup
Run these commands in the terminal
1. `cd /home/pi/`
2. `mkdir Dashboard`
3. `cd Dashboard`
4. `git clone https://github.com/murrasource/digital_dash.git`
5. `chmod +x digital_dash.py`
6. `cp /home/pi/Dashboard/digital_dash.py /home/pi/Desktop`
Now you can double click on the digital_dash.py folder on your Desktop to execute the file.

## Usage and Customization
As previously stated, my motivation for coding this was because my gas sensor broke and I didn't want to pay for the $600-$800 repair. You will see in my code that I calculate the amount of fuel left in the tank based on some simple stoichiometry. This would be incredibly simple to replace with OBD-II queries if your car's gas sensor works. Take a look here (https://python-obd.readthedocs.io/en/latest/Command%20Tables/) for a list of all the different queries the OBD library supports.

Also, feel free to have fun and customize what you want for the logo.png file. It should autoscale to the correct fit. I did my car's name in Tesla font and it looks pretty cool, if I may say so myself. The example I have on the GitHub is the Lucid Motors logo from the company's Twitter post.

**IMPORTANT TIP:** To exit fullscreen, just double click the refill button.
