"""
Module setup
"""
from setuptools import setup, find_packages

REQUIREMENTS = [
    "python-dotenv",
    "openai",
    "kubernetes",
    "locust",
]

setup(
    name="AutoChaos",
    version="0.1.0b1",
    description="Auto injecting and analyzing chaos in systems.",
    author="nervousapps (Achille Pénet)",
    author_email="achille.penet@icloud.com",
    url="https://github.com/nervousapps/AutoChaos",
    packages=find_packages(),
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.txt", "./prompts/*.txt"],
    },
    include_package_data=True,
    install_requires=REQUIREMENTS,
    entry_points={
        "console_scripts": [
            "AutoChaos = auto_chaos:main",
        ],
    },
    python_requires=">= 3.9",
)
