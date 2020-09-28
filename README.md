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
