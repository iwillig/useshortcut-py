from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="useshortcut",
    version="0.0.1",
    author="Ivan Willig, Chris Demwell",
    author_email="iwillig@gmail.com",
    description="A Python REST API client for Shortcut (formerly Clubhouse)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/iwillig/useshortcut-py",
    project_urls={
        "Bug Tracker": "https://github.com/iwillig/useshortcut-py/issues",
        "Documentation": "https://github.com/iwillig/useshortcut-py#readme",
        "Source Code": "https://github.com/iwillig/useshortcut-py",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Topic :: Office/Business :: Groupware",
        "Topic :: Software Development :: Libraries",
    ],
    packages=find_packages(exclude=["tests", "tests.*"]),
    python_requires=">=3.9",
    install_requires=[
        "requests>=2.25.0",
    ],
    extras_require={
        "dev": [
            "black>=24.0.0",
            "pytest>=8.0.0",
            "pytest-cov>=4.0.0",
            "twine>=4.0.0",
            "wheel>=0.40.0",
            "build>=0.10.0",
        ]
    },
    keywords="shortcut api client rest project-management clubhouse",
)
