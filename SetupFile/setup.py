import os
import subprocess

CURRENT_DIR = os.path.dirname(__file__)

class PathNotException(Exception):
    """Package Path Not Exist"""

domain = input("Package name: ")
target_path = os.path.abspath(f"{CURRENT_DIR}/../../{domain}")
domain_path = domain.replace(".", "/")

if not os.path.exists(target_path):
    PathNotException("Package Path Not Exist")

def _setup():
    main_path = f"{target_path}/src/{domain_path}"
    cmds = [
        f"cp ./Makefile.cfg {main_path}/Makefile",
        f"cp ./alembic.ini {main_path}/",
        f"cp ./.isort.cfg {target_path}/src/",
        f"cp -r ./models {main_path}/",
        f"cp -r ./myAlembic {main_path}/",
    ]
    for cmd in cmds:
        subprocess.call(
            cmd,
            shell=True
        )


if __name__ == "__main__":
    _setup()
