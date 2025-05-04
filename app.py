import os
from flask import Flask, render_template, request
import subprocess
import sys
import yt_dlp

# Print Python and yt-dlp versions
print(f"Python version: {sys.version}")
print(f"yt-dlp version: {yt_dlp.version.__version__}")

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
            output_filename = f"{file_name}.%(ext)s"
            try:
                result = subprocess.run([
                    "yt-dlp",
                    "--no-playlist",               # 👈 This tells yt-dlp not to treat it as a playlist
                    "-o", output_filename,
                    "-f", "best",
                    video_url
                ], check=True, capture_output=True, text=True)

                message = f"✅ Download complete: {file_name}"
            except subprocess.CalledProcessError as e:
                print("Download error:", e.stderr)  # Print to logs for debugging
                message = f"❌ Error downloading video:\n{e.stderr}"
    return render_template("index.html", message=message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
