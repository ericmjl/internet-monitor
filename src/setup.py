import setuptools

setuptools.setup(
    name="netmonitor",
    version="1.0.0",
    description="",
    long_description="",
    url="",
    author="",
    author_email="",
    license="",
    packages=["netmonitor"],
    install_requires=[
        "streamlit",
        "click",
        "tendo",
        "pandas",
        "speedtest-cli",
        "tinydb",
        "loguru",
        "schedule",
    ],
    zip_safe=False,  # install source files not egg
    entry_points={"console_scripts": ["netmonitor = netmonitor.cli:main"]},
)
