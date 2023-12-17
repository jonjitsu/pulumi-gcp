from invoke import task
from pathlib import Path

CWD = Path.cwd()

if CWD.stem == "examples":
    from examples_tasks import *
else:    
    from example_tasks import *