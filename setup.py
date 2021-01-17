import setuptools

# import sys, os

setuptools.setup(
    name="remote_screens",
    version="0.1.0",
    description="Python test package",
    long_description=open("DESCRIPTION.rst").read(),
    license="GPL v3",
    author="Oele Geirneart",
    # packages=setuptools.find_packages(),
    packages=setuptools.find_packages(include=["src", "src.*", "src.*.*"]),
    # packages=setuptools.find_packages(where="src", exclude=["tests"]),
    package_data={"src": ["description.txt"]},
    install_requires=["websocket-client", "requests", "psutil", "Xlib"],
    entry_points={"console_scripts": ["hello=src.app:main", "stup=src.app:stup"]},
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
    include_package_data=True,
)
