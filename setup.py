from setuptools import setup, find_packages

setup(
    name="cparsers",
    version="0.2.1",
    packages=find_packages("src"),
    package_dir={"": "src"},
)
