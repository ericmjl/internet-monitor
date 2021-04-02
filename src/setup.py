import setuptools
from pathlib import Path


root_dir = Path(__file__).parent.parent.absolute()
readme_path = root_dir / "README.md"

with open(readme_path, "r+") as f:
    readme = f.read()

setuptools.setup(
    name="netspeedmonitor",
    version="0.1.1",
    description="A utility for recording your internet speed.",
    long_description=readme,
    long_description_content_type="text/markdown",
    url="https://github.com/ericmjl/internet-monitor",
    author="Eric J. Ma",
    author_email="ericmajinglong@gmail.com",
    license="MIT",
    packages=["netspeedmonitor"],
    install_requires=[
        "streamlit",
        "click",
        "tendo",
        "pandas",
        "speedtest-cli",
        "tinydb",
        "loguru",
        "schedule",
        "tinyrecord",
    ],
    zip_safe=False,  # install source files not egg
    entry_points={"console_scripts": ["netspeedmonitor = netspeedmonitor.cli:main"]},
)
