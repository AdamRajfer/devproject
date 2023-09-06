from setuptools import find_packages, setup

setup(
    name="devproject",
    version="0.0.2",
    description=(
        "Tools for running projects in Visual Studio Code in devcontainers"
    ),
    author="Adam Rajfer",
    python_requires=">=3.6",
    packages=find_packages(),
    entry_points={"console_scripts": ["dev = devproject:dev"]},
)
