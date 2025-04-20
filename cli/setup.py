from setuptools import setup, find_packages

setup(
    name="asst-cli",
    version="0.1.0",
    description="Command Line Interface for the ASST AI-Driven Social Media Automation Suite",
    author="ASST Team",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "asst=cli.asst_cli:main",
        ],
    },
    install_requires=[
        "requests>=2.25.0",
    ],
    python_requires=">=3.7",
)
