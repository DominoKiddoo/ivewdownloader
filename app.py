import os
import re
import sys
from flask import Flask, render_template, request
from yt_dlp import YoutubeDL, DownloadError

# Print Python version
print(f"Python version: {sys.version}")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def download():
    message = ""
    if request.method == "POST":
        video_url = request.form.get("video_url", "").strip()
        file_name = request.form.get("file_name", "").strip()

        if not video_url or not file_name:
            message = "⚠️ Please fill in all fields."
        else:
            # Sanitize filename to remove illegal characters
            safe_file_name = re.sub(r'[^a-zA-Z0-9_-]', '_', file_name)
            output_filename = f"{safe_file_name}.%(ext)s"

            ydl_opts = {
                'format': 'bv+ba/b',
                'outtmpl': output_filename,
                'noplaylist': True,
                'quiet': True,
                'no_warnings': True,
            }

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                message = f"✅ Download complete: {safe_file_name}.mp4"
            except DownloadError as e:
                message = f"❌ Error downloading video: {str(e)}"

    return render_template("index.html", message=message)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
