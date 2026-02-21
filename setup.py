"""Setup configuration for DellGuard package"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="dellguard",
    version="0.1.0",
    author="DellGuard Team",
    description="AI-Driven Infrastructure Safety System",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eliyahus/DellGuard_Project",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=[
        "pandas",
        "numpy",
        "matplotlib",
        "ollama",
    ],
    entry_points={
        "console_scripts": [
            "dellguard=main:main",
        ],
    },
)
