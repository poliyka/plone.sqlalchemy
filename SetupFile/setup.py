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

def alter(file,old_str,new_str):
    """
    替換檔案中的字串
    :param file:檔名
    :param old_str:就字串
    :param new_str:新字串
    :return:
    """
    file_data = ""
    with open(file, "r", encoding="utf-8") as f:
        for line in f:
            if old_str in line:
                line = line.replace(old_str,new_str)
            file_data += line
    with open(file,"w",encoding="utf-8") as f:
        f.write(file_data)

def _setup(main_path):
    cmds = [
        f"cp -f ./Makefile.cfg {main_path}/Makefile",
        f"cp -f ./alembic.ini {main_path}/",
        f"cp -f ./.isort.cfg {target_path}/src/",
        f"cp -rf ./models {main_path}/",
        f"cp -rf ./Alembic {main_path}/",
    ]
    for cmd in cmds:
        subprocess.call(
            cmd,
            shell=True
        )


if __name__ == "__main__":
    main_path = f"{target_path}/src/{domain_path}"
    _setup(main_path)
    alter(f"{main_path}/models/store.py", "my.package", domain)
    alter(f"{main_path}/models/user.py", "my.package", domain)
    alter(f"{main_path}/Alembic/env.py", "my.package", domain)
    print("All Done!")
