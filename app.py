from flask import Flask, render_template_string
import os

app = Flask(__name__)

HTML_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Live Image Viewer</title>
    <style>
        body {
            font-family: Arial;
            background: #111;
            color: white;
            text-align: center;
        }
        .grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
            gap: 10px;
            padding: 20px;
        }
        img {
            width: 100%;
            height: 150px;
            object-fit: cover;
            border-radius: 10px;
        }
    </style>
</head>
<body>

<h2>📸 Live Image Viewer</h2>

<div class="grid">
{% for img in images %}
    <img src="{{ img }}" loading="lazy"
         onerror="this.style.display='none'">
{% endfor %}
</div>

</body>
</html>
"""

@app.route("/")
def index():
    file_path = os.path.join(os.path.dirname(__file__), "data.txt")
    images = []

    try:
        if os.path.exists(file_path):
            with open(file_path, "r") as file:
                for line in file:
                    url = line.strip()
                    
                    # 🔥 Force HTTPS (important fix)
                    if url.startswith("http://"):
                        url = url.replace("http://", "https://")

                    if url:
                        images.append(url)

    except Exception as e:
        return f"Error: {str(e)}"

    return render_template_string(HTML_PAGE, images=images)

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
