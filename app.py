import io
from os import abort
from pathlib import Path

from flask import Flask, redirect, url_for, render_template, request
from tokei_pie.main import draw, read_root
import json
import zipfile
import shutil
import requests
import subprocess
from tempfile import TemporaryDirectory

app = Flask(__name__)

OUTPUT_DIR = Path(__file__).with_name("repos")


def _download_repo(user: str, repo: str, branch: str) -> Path:
    url = f"http://github.com/{user}/{repo}/archive/{branch}.zip"
    app.logger.info("Downloading zip: %s", url)
    resp = requests.get(url, stream=True)
    if resp.status_code == 404:
        raise RuntimeError("Not found")
    src_dir = OUTPUT_DIR / user / f"{repo}-{branch}"
    if src_dir.exists():
        shutil.rmtree(src_dir)
    src_dir.parent.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory() as tmpdir:
        target_file = Path(tmpdir) / f"{repo}-{branch}.zip"
        with target_file.open("wb") as f:
            for chunk in resp.iter_content():
                f.write(chunk)
        with zipfile.ZipFile(target_file) as zf:
            zf.extractall(OUTPUT_DIR / user)
    return src_dir


def _render_loc_report(src_dir: Path) -> str:
    app.logger.info("Rendering code directory: %s", src_dir)
    command = ["tokei", "-o", "json"]
    result = subprocess.run(command, capture_output=True, check=True, cwd=src_dir)
    data = json.loads(result.stdout.decode())
    sectors = read_root(data)
    content = io.StringIO()
    draw(sectors, content)
    return content.getvalue()


def generate_report(user: str, repo: str, branch: str, refresh: bool = False) -> str:
    src_dir = OUTPUT_DIR / user / f"{repo}-{branch}"
    if not src_dir.exists() or refresh:
        src_dir = _download_repo(user, repo, branch)
    return _render_loc_report(src_dir)


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
