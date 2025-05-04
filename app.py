import os
from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def download():
    message = ""
    if request.method == "POST":
        video_url = request.form["video_url"]
        file_name = request.form["file_name"]

        if not video_url or not file_name:
            message = "Please fill in all fields."
        else:
            output_filename = f"{file_name}.mp4"
            try:
                subprocess.run(["yt-dlp", "-o", output_filename, "-f", "best", video_url], check=True)
                message = f"✅ Download complete: {output_filename}"
            except subprocess.CalledProcessError:
                message = "❌ Error downloading video."
    return render_template("index.html", message=message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Render provides the port
    app.run(host="0.0.0.0", port=port)
