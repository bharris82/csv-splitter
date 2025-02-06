import os
import pandas as pd
from flask import Flask, render_template, request, send_from_directory

# Initialize Flask app
app = Flask(__name__, template_folder="templates", static_folder="static")

# Ensure uploads directory exists
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Home route (Handles GET and POST)
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        if "file" not in request.files:
            return "No file part", 400
        
        file = request.files["file"]
        if file.filename == "":
            return "No selected file", 400

        # Save uploaded file
        file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
        file.save(file_path)

        # Get number of rows per file
        try:
            rows_per_file = int(request.form["rows"])
        except ValueError:
            return "Invalid row number", 400

        # Process CSV file and split it
        df = pd.read_csv(file_path)
        split_files = []

        for i, chunk in enumerate(range(0, len(df), rows_per_file)):
            df_chunk = df.iloc[chunk:chunk + rows_per_file]
            chunk_filename = f"split_file_{i+1}.csv"
            chunk_path = os.path.join(app.config["UPLOAD_FOLDER"], chunk_filename)
            df_chunk.to_csv(chunk_path, index=False)
            split_files.append(chunk_filename)

        return render_template("index.html", files=split_files)

    return render_template("index.html", files=None)

# Route to serve split files for download
@app.route("/uploads/<filename>")
def uploaded_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Ensure it uses Render's PORT
    app.run(host="0.0.0.0", port=port)  # Correct port binding
