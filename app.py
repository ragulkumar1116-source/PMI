from flask import Flask, Response, abort
import requests
import os

app = Flask(__name__)

# 🔹 Load file safely
FILE_PATH = os.path.join(os.path.dirname(__file__), "data.txt")

if not os.path.exists(FILE_PATH):
    raise Exception("data.txt file not found!")

with open(FILE_PATH, "r") as f:
    links = [line.strip() for line in f if line.strip()]

# 🔹 Use filename as ID
link_map = {}
for link in links:
    try:
        filename = os.path.basename(link)
        photo_id = filename.split(".")[0]
        link_map[photo_id] = link
    except:
        continue


# 🔹 Proxy Route (IMPORTANT FIXED)
@app.route('/photo/<photo_id>')
def get_photo(photo_id):
    url = link_map.get(photo_id)

    if not url:
        abort(404)

    try:
        r = requests.get(url, stream=True, timeout=5)

        if r.status_code != 200:
            abort(404)

        return Response(
            r.iter_content(chunk_size=1024),
            content_type=r.headers.get('Content-Type', 'image/jpeg'),
            headers={
                "Cache-Control": "public, max-age=86400",
                "Access-Control-Allow-Origin": "*"
            }
        )

    except Exception as e:
        return f"Error: {str(e)}", 500


# 🔹 Gallery Page (HTTPS SAFE)
@app.route('/')
def gallery():
    html = """
    <html>
    <head>
        <title>Photo Gallery</title>
    </head>
    <body>
        <h2>Photo Gallery</h2>
    """

    for photo_id in link_map:
        html += f'''
        <img src="/photo/{photo_id}" width="120" loading="lazy" style="margin:5px;">
        '''

    html += "</body></html>"
    return html


# 🔹 Run (LOCAL HTTPS FIX)
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)