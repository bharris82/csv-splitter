import os
from flask import Flask, render_template

# Initialize Flask app and set template folder
app = Flask(__name__, template_folder="templates")

# Define route for the home page
@app.route("/")
def index():
    return render_template("index.html")  # Ensure 'index.html' is in the 'templates/' folder

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Get port from Render, default to 5000
    app.run(host="0.0.0.0", port=port)  # Bind to 0.0.0.0 for Render compatibility

