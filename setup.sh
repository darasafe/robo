#!/bin/bash

# Update the system
echo "Updating system..."
sudo apt update && sudo apt upgrade -y

# Install required packages
echo "Installing Python, Git, OpenCV, and other dependencies..."
sudo apt install -y python3 python3-pip python3-opencv libhdf5-dev \
libatlas-base-dev gfortran curl git

# Install MediaPipe (for Raspberry Pi)
echo "Installing MediaPipe for Raspberry Pi..."
pip3 install mediapipe-rpi4 --extra-index-url https://google-coral.github.io/py-repo/

# Install Adafruit Crickit library
echo "Installing Adafruit Blinka and Crickit library..."
pip3 install adafruit-blinka adafruit-circuitpython-crickit

# Install additional dependencies for the OAK-1 camera
echo "Installing DepthAI SDK..."
pip3 install depthai

# Setup Git repository (if not already initialized)
if [ ! -d ".git" ]; then
    echo "Initializing Git repository..."
    git init
fi

# Add the remote repository (replace with your GitHub repo)
echo "Setting GitHub remote..."
git remote add origin https://github.com/darasafe/robo.git

# Add and commit files to Git
echo "Adding and committing files to Git..."
git add .
git commit -m "Initial commit with project setup"

# Push to GitHub (assuming SSH is set up)
echo "Pushing code to GitHub..."
git push -u origin master

echo "Setup complete!"
