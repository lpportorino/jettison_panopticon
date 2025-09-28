#!/usr/bin/env python
"""Setup script for Panopticon."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="panopticon",
    version="1.0.0",
    author="Your Name",
    description="High-performance monitoring and control system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/panopticon",
    packages=find_packages(where="src") + ["c_data_python_bindings"],
    package_dir={
        "": "src",
        "c_data_python_bindings": "c_data_python_bindings"
    },
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "panopticon=src.run:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.12",
    ],
)