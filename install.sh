#!/usr/bin/env bash
sudo apt-get update
sudo apt-get install build-essential cmake libopenblas-dev liblapack-dev libx11-dev libgtk-3-dev python3 python3-dev python3-pip python3-tk git
pip3 install opencv-python face_recognition
cd BrickHackV
python install setup.py
