"""Rebuild the paper's figures from this project's saved sources.
Usage: python ccfa-workfiles/figures/source/rebuild.py
Dependencies: requirements.txt next to this file and the drawio desktop CLI.
The main figure is exported from its native draw.io source, preserving edits.
"""
from pathlib import Path
import runpy
BASE=Path(__file__).resolve().parents[1]
ROOT=BASE.parents[1]
for task in ['slot-interference','cache-dissociation','logit-interpolation']:
    runpy.run_path(str(BASE/task/'source/plot.py'),run_name='__main__')
runpy.run_path(str(BASE/'method-overview/source/export_drawio.py'),run_name='__main__')
