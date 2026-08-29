import os
import runpy
import sys

if getattr(sys, "frozen", False):
    base_dir = sys._MEIPASS
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(base_dir)

runpy.run_path(
    os.path.join(base_dir, "main.py"),
    run_name="__main__"
)
