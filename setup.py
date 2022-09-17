import os
import setuptools

cwd = os.getcwd()


def long_description() -> str:
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


def requirements() -> list[str]:
    with open(cwd + "/requirements.txt", "r") as file:
        return [line.strip() for line in file.read().split("\n") if line.strip()]


setuptools.setup(
    name="python-multibar",
    version="4.0.0",
    keywords=[
        "PYTHON",
        "PYTHON3",
        "PROGRESS",
        "PROGRESSBAR",
        "PROGRESSBARS",
        "PROGRESS BAR",
        "PROGRESS BARS",
    ],
    author="DenyS",
    description="Flexible wrapper for static progressbar writing.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    license="Apache License, Version 2.0",
    install_requires=requirements(),
    packages=setuptools.find_namespace_packages(include=["multibar*"]),
    url="https://github.com/Animatea/python-multibar",
    download_url="https://github.com/Animatea/python-multibar/archive/refs/heads/master.zip",
    project_urls={
        "Documentation": "https://animatea.github.io/python-multibar/",
        "Bug Tracker": "https://github.com/Animatea/python-multibar/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: Apache Software License",
        "Typing :: Typed",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    package_data={"multibar": ["py.typed"]},
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.9",
)
