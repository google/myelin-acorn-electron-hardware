import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arcflash",
    version="0.1.3",
    author="Phillip Pearson",
    author_email="pp@myelin.nz",
    description="Python support libraries for Arcflash flash ROM board for Acorn computers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/google/myelin-acorn-electron-hardware/tree/main/a3000_rom_emulator/python_lib",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[
        "protobuf",
        "PySerial",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    entry_points={'console_scripts': ['arcflash = arcflash.main:main']},
)
