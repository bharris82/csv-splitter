import os
import zipfile
from typing import List

import pandas as pd
from flask import (
    Flask,
    render_template,
    request,
    send_from_directory,
    redirect,
    url_for,
)
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")

# Ensure uploads directory exists
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

ALLOWED_EXTENSIONS = {"csv"}
MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10MB

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config["MAX_CONTENT_LENGTH"] = MAX_CONTENT_LENGTH

# Helpers
def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route (Handles GET and POST)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400
        
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400

        if not allowed_file(file.filename):
            return "Invalid file type", 400

        filename = secure_filename(file.filename)

        # Save uploaded file
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(file_path)

        # Get number of rows per file
        try:
            rows_per_file = int(request.form["rows"])
        except ValueError:
            return "Invalid row number", 400

        if rows_per_file <= 0:
            return "Rows must be positive", 400

        split_column = request.form.get("split_column") or None
        zip_output = request.form.get("zip_output") == "on"

        split_files: List[str] = []

        if split_column:
            try:
                df = pd.read_csv(file_path)
            except Exception:
                return "Failed to read CSV", 400

            if split_column not in df.columns:
                return f"Column '{split_column}' not found", 400

            for value, df_chunk in df.groupby(split_column):
                chunk_filename = f"{secure_filename(str(value))}.csv"
                chunk_path = os.path.join(app.config["UPLOAD_FOLDER"], chunk_filename)
                df_chunk.to_csv(chunk_path, index=False)
                split_files.append(chunk_filename)
        else:
            try:
                for i, chunk in enumerate(pd.read_csv(file_path, chunksize=rows_per_file)):
                    chunk_filename = f"split_file_{i+1}.csv"
                    chunk_path = os.path.join(app.config["UPLOAD_FOLDER"], chunk_filename)
                    chunk.to_csv(chunk_path, index=False)
                    split_files.append(chunk_filename)
            except Exception:
                return "Failed to read CSV", 400

        if zip_output and split_files:
            zip_name = "split_files.zip"
            zip_path = os.path.join(app.config["UPLOAD_FOLDER"], zip_name)
            with zipfile.ZipFile(zip_path, "w") as zf:
                for fname in split_files:
                    zf.write(os.path.join(app.config["UPLOAD_FOLDER"], fname), fname)
            split_files = [zip_name]

        return render_template("index.html", files=split_files)

    return render_template("index.html", files=None)

# Route to serve split files for download
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))  # Ensure it uses Render's PORT
    app.run(host="0.0.0.0", port=port)  # Correct port binding
