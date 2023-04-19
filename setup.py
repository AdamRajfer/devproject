from setuptools import find_packages, setup

setup(
    name="devproject",
    version="0.0.1",
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
