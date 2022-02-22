import os
import setuptools

cwd = os.getcwd()


def long_description() -> str:
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


setuptools.setup(
    name="python-multibar",
    version="3.0.2",
    keywords=[
        "PYTHON",
        "PYTHON3",
        "DISCORD",
        "DISCORD-API",
        "PROGRESS",
        "PROGRESSBARS",
        "PROGRESS BAR",
        "PROGRESS BARS",
        "SYNC",
        "ASYNC",
    ],
    author="DenyS",
    description="Basic wrapper for static writing progress bars.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    license="Apache License, Version 2.0",
    packages=setuptools.find_namespace_packages(include=["multibar*"]),
    url="https://github.com/Animatea/python-multibar",
    download_url="https://github.com/Animatea/python-multibar/archive/refs/heads/master.zip",
    project_urls={
        "Documentation": "https://animatea.github.io/python-multibar/",
        "Bug Tracker": "https://github.com/Animatea/python-multibar/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries",
        "Programming Language :: Python :: Implementation :: CPython",
        "License :: OSI Approved :: Apache Software License",
        "Intended Audience :: Other Audience",
        "Framework :: AsyncIO",
        "Typing :: Typed",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Topic :: Utilities",
    ],
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
)
