from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="useshortcut",
    version="0.0.1",
    author="Ivan Willig, Chris Demwell",
    author_email="iwillig@gmail.com",
    description="A REST client for the Shortcut REST API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iwillig/useshortcut-py",
    project_urls={
        "Bug Tracker": "https://github.com/iwillig/useshortcut-py/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    packages=find_packages(),
    python_requires=">=3.13",
    install_requires=[
        "requests>=2.32.3",
        "click>=8.1.8",
    ],
    entry_points={
        "console_scripts": [
            "shortcut-cli=cli:cli",
        ],
    },
)
