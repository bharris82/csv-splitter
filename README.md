# CSV Splitter

This repository contains a small Flask application used to split uploaded CSV
files into smaller chunks. The application was created as a simple example but
has been expanded with a few quality of life improvements such as basic input
validation, optional column based splitting, zipped downloads and automated
tests.

## Requirements

Install the dependencies from `requirements.txt` using `pip`:

```bash
pip install -r requirements.txt
```

## Running The Application

```bash
export FLASK_APP=SplittyWeb.py
flask run
```

By default the application listens on port `5000`. When deployed to a hosting
provider the `PORT` environment variable can be used to change the port.

## Usage

1. Navigate to the index page.
2. Upload a CSV file and specify the number of rows for each output file.
3. *(Optional)* Enter a column name to split by unique values instead of row
   counts.
4. *(Optional)* Select the "Zip output" checkbox to download a compressed
   archive.
5. Submit the form and download the generated files from the links provided.

## Testing

Tests use `pytest`. Run them with:

```bash
python -m pytest
```

The tests exercise both GET and POST requests and verify that CSV files are
split correctly.

