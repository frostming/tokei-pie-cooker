import io
import json
import os
import shutil
import subprocess
import zipfile
from pathlib import Path
from tempfile import TemporaryDirectory

import requests
from cachecontrol.caches import FileCache
from flask import Flask, abort, redirect, render_template, request, url_for
from tokei_pie.main import draw, read_root

app = Flask(__name__)
OUTPUT_DIR = Path(__file__).with_name("repos")
CACHE_DIR = Path(__file__).with_name(".caches")
cached = FileCache(CACHE_DIR.as_posix())


def _get_loc(user: str, repo: str, branch: str) -> bytes:
    url = f"http://github.com/{user}/{repo}/archive/{branch}.zip"
    app.logger.info("Downloading zip: %s", url)
    resp = requests.get(url, stream=True)
    if resp.status_code == 404:
        raise RuntimeError("Not found")
    with TemporaryDirectory() as tmpdir:
        target_file = Path(tmpdir) / f"{repo}-{branch}.zip"
        with target_file.open("wb") as f:
            for chunk in resp.iter_content():
                f.write(chunk)
        with zipfile.ZipFile(target_file) as zf:
            zf.extractall(tmpdir)
        src_dir = os.path.join(tmpdir, f"{repo}-{branch}")
        command = ["tokei", "-o", "json"]
        result = subprocess.run(command, capture_output=True, check=True, cwd=src_dir)
        shutil.rmtree(src_dir)
        return result.stdout


def generate_report(user: str, repo: str, branch: str, refresh: bool = False) -> str:
    fkey = f"{user}/{repo}/{branch}"
    if refresh:
        cached.delete(fkey)
    data = cached.get(fkey)
    if data is None:
        data = _get_loc(user, repo, branch)
        cached.set(fkey, data)
    sectors = read_root(json.loads(data))
    buffer = io.StringIO()
    draw(sectors, buffer)
    return buffer.getvalue()


@app.get("/<user>/<repo>/<branch>")
def repo_pie(user: str, repo: str, branch: str):
    refresh = request.args.get("refresh")
    if not branch:
        return redirect(
            url_for("repo_pie", user=user, repo=repo, branch="master", refresh=refresh)
        )
    try:
        return generate_report(user, repo, branch, refresh)
    except RuntimeError:
        abort(404)


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html")
    repo_string = request.form.get("r")
    return redirect(url_for("index") + repo_string)
