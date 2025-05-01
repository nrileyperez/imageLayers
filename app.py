import os, threading
from uuid import uuid4
from flask import (
    Flask, render_template, request,
    send_from_directory, url_for, jsonify, redirect
)
import cv2, numpy as np
from skimage.feature import canny
from skimage.transform import probabilistic_hough_line
from sklearn.cluster import KMeans
from PIL import Image

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'output'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# In-memory job store
# jobs[job_id] = {
#   'progress': int(0–100),
#   'original': filename,
#   'segments': [filenames…]
# }
jobs = {}


def remove_background(img):
    # … your existing grabCut logic …
    mask = np.zeros(img.shape[:2], np.uint8)
    rect = (10,10, img.shape[1]-20, img.shape[0]-20)
    bgd, fgd = np.zeros((1,65),np.float64), np.zeros((1,65),np.float64)
    cv2.grabCut(img, mask, rect, bgd, fgd, 5, cv2.GC_INIT_WITH_RECT)
    return np.where((mask==2)|(mask==0), 0, 1).astype('uint8')


def run_segmentation(job_id, upload_path, n_layers):
    img = cv2.imread(upload_path)
    h, w = img.shape[:2]

    # total steps = 4 prep steps + one per layer
    total_steps = 4 + n_layers
    step_pct    = 100.0 / total_steps
    progress    = 0.0

    # 1) Background removal
    fg = remove_background(img)
    progress += step_pct
    jobs[job_id]['progress'] = int(progress)

    # 2) Edge detection
    gray  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = canny(gray, sigma=2)
    progress += step_pct
    jobs[job_id]['progress'] = int(progress)

    # 3) Hough line detection
    lines = probabilistic_hough_line(
        edges,
        threshold=10,
        line_length=max(w//4,50),
        line_gap=3
    )
    progress += step_pct
    jobs[job_id]['progress'] = int(progress)

    # 4) Cluster boundaries
    ys = [(y0+y1)/2 for ((x0,y0),(x1,y1)) in lines if abs(y1-y0)<5]
    ys_arr = np.array(ys).reshape(-1,1)
    if len(ys) < n_layers - 1:
        bounds = [int(i*h/n_layers) for i in range(n_layers+1)]
    else:
        km = KMeans(n_clusters=n_layers-1, random_state=0).fit(ys_arr)
        centers = sorted(int(c[0]) for c in km.cluster_centers_)
        bounds = [0] + centers + [h]
    progress += step_pct
    jobs[job_id]['progress'] = int(progress)

    # 5) Slice out each layer—one step per slice
    segments = []
    for i in range(n_layers):
        y0, y1 = bounds[i], bounds[i+1]
        mask = np.zeros((h,w), np.uint8); mask[y0:y1,:] = 1
        combo = (mask & fg)*255
        band  = cv2.bitwise_and(img, img, mask=combo)

        pil = Image.fromarray(cv2.cvtColor(band, cv2.COLOR_BGR2RGB))
        pil.putalpha(Image.fromarray(combo))
        fname = f"{uuid4().hex}_layer{i+1}.png"
        path  = os.path.join(app.config['UPLOAD_FOLDER'], fname)
        pil.save(path)
        segments.append(fname)

        # update after each slice
        progress += step_pct
        jobs[job_id]['progress'] = min(100, int(progress))

    # finalize
    jobs[job_id]['segments'] = segments
    jobs[job_id]['progress'] = 100


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/start', methods=['POST'])
def start():
    f = request.files['image']
    layers = int(request.form.get('layers', 3))
    # Save upload
    ext = os.path.splitext(f.filename)[1]
    original = f"{uuid4().hex}{ext}"
    upath = os.path.join(app.config['UPLOAD_FOLDER'], original)
    f.save(upath)

    # Init job
    job_id = uuid4().hex
    jobs[job_id] = {
      'progress': 0,
      'original': original,
      'segments': []
    }

    # Fire background thread
    thread = threading.Thread(
      target=run_segmentation,
      args=(job_id, upath, layers),
      daemon=True
    )
    thread.start()

    # Return job ID to client
    return jsonify(job_id=job_id)


@app.route('/progress/<job_id>')
def progress(job_id):
    job = jobs.get(job_id)
    if not job:
        return jsonify(error="Unknown job"), 404
    return jsonify(progress=job['progress'])


@app.route('/results/<job_id>')
def results(job_id):
    job = jobs.get(job_id)
    if not job or job['progress'] < 100:
        return redirect(url_for('index'))
    return render_template(
      'results.html',
      original=url_for('uploaded_file', filename=job['original']),
      segments=job['segments']
    )


@app.route('/output/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
if __name__ == '__main__':
    # starts the Flask dev server on http://127.0.0.1:5000
    app.run(debug=True)
