from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="bookreturncalculator",
    version="0.0.3",
    author="Alfi",
    author_email="alfithomas2002@gmail.com",
    description="A library for calculating book return due dates.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(include=['bookreturncalculatorPkg']),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
