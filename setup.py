#!/usr/bin/env python3

from setuptools import setup

setup(
    name="eloh",
    version="0.0.1",
    author="Louis Abraham",
    license="MIT",
    author_email="louis.abraham@yahoo.fr",
    description="Send files via hole-punching",
    python_requires=">=3.6",
    packages=["eloh"],
    entry_points={
        "console_scripts": [
            "eloh-server = eloh.server:main",
            "eloh-send = eloh.client:send_cli",
            "eloh-recv = eloh.client:recv_cli",
        ]
    },
)

