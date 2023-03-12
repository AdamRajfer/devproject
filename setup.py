from setuptools import find_packages, setup

setup(
    name="devproject",
    version="0.0.1",
    description=(
        "Tools for running projects in Visual Studio Code in devcontainers"
    ),
    author="Adam Rajfer",
    install_requires=["argcomplete", "pandas", "tabulate"],
    python_requires=">=3.6",
    packages=find_packages("src"),
    package_dir={"": "src"},
    package_data={
        "": ["data/*", "data/.bashrc", "data/.bash_logout", "data/.profile"]
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "dev = devproject:dev",
        ]
    }
)
