# 🍰 Image Segmentation App

**A Flask-powered web app that cleanly extracts and exports individual layers (or objects) from an image, with real-time progress tracking.**

---

## 🔍 Overview

This project demonstrates a full-stack Python solution for image segmentation:

- **Background removal** via OpenCV GrabCut  
- **Layer boundary detection** using Canny + Probabilistic Hough  
- **Clustering & slicing** to produce transparent PNG layers  
- **Accurate progress bar** implemented with background threads and client-side polling  
- **Clean, responsive UI** built with Flask templates and modern CSS  

---

## 🚀 Features

- **Upload any image** and specify N layers  
- **Real-time progress bar** shows percentage complete  
- **Transparent PNG exports** for each segment (ideal for UI/UX or web design)  
- **Automatic cleanup** of old outputs to avoid stale files  
- **Easy to extend**: swap in SLIC, watershed, or deep-learning backends  

---

## 🛠 Tech Stack

- **Backend**: Python 3.8+, Flask  
- **Image Processing**: OpenCV, scikit-image, scikit-learn, Pillow  
- **Frontend**: HTML5, CSS3 (modern dark theme), vanilla JS for progress polling  
- **Dev Tools**: Git, virtualenv, PyCharm / VSCode  

---

## 📥 Installation

1. **Clone** this repo:  
   ```bash
   git clone https://github.com/<YOUR_USERNAME>/image-segmentation-app.git
   cd image-segmentation-app
