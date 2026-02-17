from setuptools import find_packages, setup

setup(
    name="movieRecommendation",
    version="0.0.1",
    author="SiddhuShkya",
    author_email="siddhuushakyaa@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[],
)
