# 🖱️ Virtual Mouse Gesture Detector

A computer vision-based system that enables touchless mouse control using hand gestures captured via a webcam. Built with Python, MediaPipe, and PyAutoGUI, this tool simulates mouse movements and clicks, and even takes screenshots—all through intuitive hand gestures.

---

## 🚀 Features

- 🖐️ Real-time hand gesture recognition using webcam
- 🖱️ Simulate mouse actions:
  - Cursor movement
  - Left click, Right click, Double click
  - Scroll up and down
  - Take screenshot
- ☁️ Screenshots auto-uploaded to **Cloudinary**
- 🧠 Built with **MediaPipe**, **OpenCV**, **PyAutoGUI**, and **Streamlit** (if using web UI)

---

## 🎯 Motivation

In the evolving landscape of human-computer interaction, traditional input devices like the mouse and keyboard are being complemented—or replaced—by more intuitive, contactless technologies.

This project addresses the increasing demand for **touchless interfaces**, especially in hygiene-conscious or accessibility-focused settings, by offering a software-only solution requiring only a webcam and Python.

---

## 🧰 Technologies Used

- **Python 3.8+**
- [MediaPipe](https://github.com/google/mediapipe) – for hand detection and landmark extraction
- **OpenCV** – image processing and frame handling
- **PyAutoGUI** – for controlling mouse actions
- **Cloudinary** – for cloud storage of screenshots
- **Streamlit** *(optional)* – for user interface

---

## 🛠️ Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/virtual-mouse-gesture-detector.git
cd virtual-mouse-gesture-detector
