import os
import tempfile
import webbrowser
import pandas as pd
from typing import Dict
from .indicator import Indicator
from .utils import is_in_jupyter
from jinja2 import Environment, FileSystemLoader

_JUPYTER = is_in_jupyter()
_ENV = Environment(
    keep_trailing_newline=True,
    trim_blocks=True,
    lstrip_blocks=True,
    loader=FileSystemLoader(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "templates")
    ),
)


def _temp_html_file(html: str):
    fd, path = tempfile.mkstemp(suffix=".html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)
    return path


def open_html(html: str):
    path = _temp_html_file(html)
    if _JUPYTER:
        webbrowser.open("file://" + path)
    else:
        webbrowser.open(path)


def render_html(context: Dict):
    context["in_jupyter"] = _JUPYTER
    template = _ENV.get_template("chart.html")
    html = template.render(context)
    open_html(html)
