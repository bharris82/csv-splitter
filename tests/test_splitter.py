import io
import os
import zipfile

import pandas as pd
import pytest

from SplittyWeb import app


def create_csv():
    return "col1,col2\na,1\nb,2\nc,3\nd,4\n"


def test_split_rows(tmp_path):
    app.config["UPLOAD_FOLDER"] = tmp_path.as_posix()
    client = app.test_client()

    data = {
        "file": (io.BytesIO(create_csv().encode("utf-8")), "data.csv"),
        "rows": "2",
    }
    resp = client.post("/", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    assert (tmp_path / "split_file_1.csv").exists()
    assert (tmp_path / "split_file_2.csv").exists()


def test_split_by_column(tmp_path):
    app.config["UPLOAD_FOLDER"] = tmp_path.as_posix()
    client = app.test_client()

    csv_data = "group,val\nA,1\nB,2\nA,3\n"
    data = {
        "file": (io.BytesIO(csv_data.encode("utf-8")), "data.csv"),
        "rows": "1",
        "split_column": "group",
    }
    resp = client.post("/", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    assert (tmp_path / "A.csv").exists()
    assert (tmp_path / "B.csv").exists()


def test_zip_output(tmp_path):
    app.config["UPLOAD_FOLDER"] = tmp_path.as_posix()
    client = app.test_client()
    data = {
        "file": (io.BytesIO(create_csv().encode("utf-8")), "data.csv"),
        "rows": "2",
        "zip_output": "on",
    }
    resp = client.post("/", data=data, content_type="multipart/form-data")
    assert resp.status_code == 200
    zip_path = tmp_path / "split_files.zip"
    assert zip_path.exists()
    with zipfile.ZipFile(zip_path) as zf:
        assert set(zf.namelist()) == {"split_file_1.csv", "split_file_2.csv"}

