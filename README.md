# digital_dash
A digital dashboard using Python, PyQt, Raspberry Pi Zero W, and vehicle's On Board Diagnostics (OBD-II) Port.

## Motivation
My personal reason for creating this was because my car's fuel sensor broke. The cost for repair was astronomical, so I figured creating a program to calculate the fuel level and milage would be much cheaper.

Really, though, this is easily made into just a fun digital dashboard for anyone who wants to experiment with 'carputers.'

## How It Works
The real guts of this operation is in the OBD-II port of pretty much every car since the 1990s. OBD (On Board Diagnostics) lets you access the car's computer and retrieve information from it. Scroll down to see my supplies list.

Every tenth of a second, the program queries the OBD port for the data I want through the obd python library. Dependencies are also listed below.
