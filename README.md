# 🤖 Robo

### **A DIY Buddy Robot**  
Welcome to **Robo** – your friendly, customizable companion robot project! Built using Raspberry Pi, OAK-1 camera, and Crickit HAT, Robo is designed to help you explore the world of robotics and computer vision.

---

## 🚀 Features
- **Hand Gesture Recognition**: Uses OAK-1 and MediaPipe to identify hand gestures.
- **Servo Motor Control**: Integrated with the Crickit HAT for smooth movement.
- **AI-Powered Vision**: OAK-1 camera enables real-time object and gesture tracking.
- **Extensible Framework**: Easily adaptable to add more sensors, functions, or behavior.

---

## 🛠️ Hardware Requirements
- **Raspberry Pi 4 Model B** (or 3 Model B, but slower)
- **OAK-1 Camera** by Luxonis  
- **Adafruit Crickit HAT** for Raspberry Pi  
- **Micro SD Card** with Buster OS  
- Power Supply, HDMI Cable, Monitor, Keyboard, and Mouse

---

## 🧑‍💻 Software Requirements
- Python 3.9+
- MediaPipe
- OpenCV
- DepthAI SDK
- Adafruit Blinka & CircuitPython libraries

---

## 📦 Setup
Follow these steps to set up your Robo robot.

1. Flash Raspberry Pi OS **Buster** on SD card.
2. Connect OAK-1 via USB and Cricket HAT via GPIO.
3. Clone this repo on the Pi:
   ```bash
   git clone https://github.com/darasafe/robo.git
   cd robo
   bash setup.sh
4. Run:
   ```bash
   app.py
5. Interface with the robot using the robot-control repository
