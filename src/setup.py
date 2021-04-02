import setuptools

setuptools.setup(
    name="netspeedmonitor",
    version="0.1.0",
    description="A utility for recording your internet speed.",
    long_description="",
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
