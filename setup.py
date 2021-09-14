import os
import re
import typing
import setuptools


cwd: str = os.getcwd()
keywords: typing.List[str] = [
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
]


def long_description() -> str:
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()


def parse_requirements() -> typing.List[str]:
    with open(cwd + "/requirements.txt", "r", encoding="utf-8") as file:
        return [d.strip() for d in file.read().split("\n") if d.strip()]


def parse_metadata() -> typing.Dict[str, str]:
    with open(cwd + "/multibar/_about.py", "r", encoding="utf-8") as file:
        data = file.read()

    pattern: re.Pattern[str] = re.compile(r"""^__(?P<key>\w+)__.*"(.+)\"""", re.MULTILINE)

    groups: typing.Dict[str, str] = {}
    for match in pattern.findall(data):
        groups.update({match[0]: match[1]})

    return groups


metadata: typing.Dict[str, str] = parse_metadata()


setuptools.setup(
    name=metadata["title"],
    version="2.0.6",
    keywords=keywords,
    author=metadata["author"],
    description="Basic wrapper for static writing progress bars.",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    license=metadata["license"],
    packages=setuptools.find_namespace_packages(include=["multibar*"]),
    install_requires=parse_requirements(),
    url="https://github.com/Animatea/python-multibar",
    download_url="https://github.com/Animatea/python-multibar/archive/refs/heads/master.zip",
    project_urls={
        "Documentation": "https://app.gitbook.com/@denys111/s/python-multibar/",
        "Examples": "https://github.com/Animatea/python-multibar/tree/master/examples",
        "Bug Tracker": "https://github.com/Animatea/python-multibar/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Environment :: Console",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
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
    test_suite="tests",
    include_package_data=True,
    zip_safe=False,
    python_requires=">=3.8",
)
