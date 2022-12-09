from setuptools import setup
import os

VERSION = "0.21"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="kgcreator",
    description="Knowledge Graph Creator: converts text to RDF triples",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Mark Watson",
    url="https://github.com/mark-watson/kgcreator",
    project_urls={
        "Issues": "https://github.com/mark-watson/kgcreator/issues",
        "CI": "https://github.com/mark-watson/kgcreator/actions",
        "Changelog": "https://github.com/mark-watson/kgcreator/releases",
    },
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["kgcreator"],
    entry_points="""
        [console_scripts]
        kgcreator=kgcreator.cli:cli
    """,
    install_requires=["click", "spacy"],
    extras_require={
        "test": ["pytest"]
    },
    python_requires=">=3.7",
)
