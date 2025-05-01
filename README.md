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
   ```
2. Create & activate a virtual environment:<br>
Windows powershell
      ```bash
      python -m venv .venv
      .\.venv\Scripts\Activate.ps1
      ```
macOS / Linux
   ```bash
      python3 -m venv .venv
      source .venv/bin/activate
   ```
3. Install Dependencies
   ```bash
      pip install -r requirements.txt
   ```
4. Run the app:
   ```bash
      python app.py
   ```
## Project Structure
 ```bash
     image-segmentation-app/
├── app.py               # Flask routes & segmentation logic
├── requirements.txt     # Python dependencies
├── templates/
│   ├── index.html       # Upload form + progress polling
│   └── results.html     # Segmented-layer display
├── static/
│   └── style.css        # Modern dark-theme CSS
├── output/              # Auto-generated PNGs (gitignored)
└── README.md            # This file

   ```
## Future Work
- Swap in SLIC superpixels or watershed algorithms for more organic masks
- Add SVG export using OpenCV contour tracing
- Integrate Celery + Redis for production-grade async jobs
- Dockerize and deploy via GitHub Actions & Heroku / Docker Hub
