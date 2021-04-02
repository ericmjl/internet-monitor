import setuptools

setuptools.setup(
    name="netspeedmonitor",
    version="1.0.0",
    description="",
    long_description="",
    url="",
    author="",
    author_email="",
    license="",
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
