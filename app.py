from flask import Flask, Response, abort
import requests
import os

app = Flask(__name__)

# 🔹 Load file safely
FILE_PATH = os.path.join(os.path.dirname(__file__), "data.txt")

if not os.path.exists(FILE_PATH):
    raise FileNotFoundError("data.txt file not found!")

with open(FILE_PATH, "r") as f:
    links = [line.strip() for line in f if line.strip()]

# 🔹 Map photo_id -> URL
link_map = {}
for link in links:
    try:
        filename = os.path.basename(link)
        photo_id = filename.split(".")[0]
        link_map[photo_id] = link
    except Exception:
        continue

# 🔹 Proxy route
@app.route('/photo/<photo_id>')
def get_photo(photo_id):
    url = link_map.get(photo_id)
    if not url:
        abort(404)
    try:
        r = requests.get(url, stream=True, timeout=5)
        if r.status_code != 200:
            abort(404)
        content_type = r.headers.get('Content-Type', 'image/jpeg')
        return Response(
            r.iter_content(chunk_size=1024),
            content_type=content_type,
            headers={
                "Cache-Control": "public, max-age=86400",
                "Access-Control-Allow-Origin": "*"
            }
        )
    except requests.RequestException as e:
        return f"Error fetching image: {str(e)}", 500

# 🔹 Gallery page
@app.route('/')
def gallery():
    html = "<html><head><title>Photo Gallery</title></head><body><h2>Photo Gallery</h2>"
    for photo_id in link_map:
        html += f'<img src="/photo/{photo_id}" width="120" loading="lazy" style="margin:5px;">'
    html += "</body></html>"
    return html

# ✅ Do NOT include app.run() for Render deployment
# Render will use Gunicorn: gunicorn app:app --workers 3
