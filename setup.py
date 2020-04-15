import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="alt-tabpy",
    version="0.0.2",
    author="Will Ayd",
    author_email="will_ayd@innobi.io",
    description="A lightweight TabPy implementation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://alttabpy.readthedocs.io/en/latest/index.html",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=['tornado'],
)
