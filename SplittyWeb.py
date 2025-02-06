from flask import Flask, request, render_template
import pandas as pd
import os

app = Flask(__name__)

# Upload folder
UPLOAD_FOLDER = "uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get user input
        rows_per_file = int(request.form["rows"])
        file = request.files["file"]

        if file:
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
            file.save(file_path)
            
            # Read and split CSV
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

if __name__ == "__main__":
    app.run(debug=True)
