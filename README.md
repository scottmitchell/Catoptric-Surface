# Catoptric Surface

This repo contains code for controlling the prototype **Catoptric Surface**, an InCEES-funded robotic facade research project at Washington University in St. Louis.

## Setup

### Controlling the surface via ssh

**macOS**
- Make sure you have X installed (https://www.xquartz.org/)
- Connect to wustl wifi
- Open terminal
- Navigate to the Catoptric folder
- source catoptric_ve/bin/activate
- cd Catoptric-Surface
- python CatoptricSurface.py

## Send files to Raspberry Pi (Catoptric Controller)
- `scp -P 2222 <path to file> "<IP of Raspberry pi>:~/repos/Catoptric-Surface/Catoptric-Surface/csv/new"`
