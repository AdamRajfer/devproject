import os
import subprocess

from setuptools import find_packages, setup

setup(
    name="devproject",
    version=subprocess.check_output("git rev-parse HEAD", shell=True, cwd=os.path.dirname(__file__)).decode("utf-8").strip(),
    description=(
        "Tools for running projects in Visual Studio Code in devcontainers"
    ),
    author="Adam Rajfer",
    python_requires=">=3.6",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={"": ["data/*"]},
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "dev = devproject:dev",
        ]
    }
)
