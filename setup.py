#!/usr/bin/env python3
"""
Setup script for the Qdrant Multi-Node Cluster Demo package.
"""

from setuptools import setup, find_packages

setup(
    name="qdrant-demo",
    version="0.1.0",
    description="A demonstration of deploying Qdrant in a multi-node cluster setup",
    author="Mohit Kumar",
    author_email="your.email@example.com",
    url="https://github.com/Mohitkr95/qdrant-multi-node-cluster",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.8",
    install_requires=[
        "qdrant-client==1.6.1",
        "numpy==1.24.3",
        "rich==13.6.0",
    ],
    entry_points={
        "console_scripts": [
            "qdrant-demo=run_demo:main",
        ],
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
) 