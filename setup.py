from os import path
import setuptools


SCRIPT_DIR = path.abspath(path.dirname(__file__))
with open(path.join(SCRIPT_DIR, 'README.md')) as f:
    long_description = f.read()


setuptools.setup(
    name="ShenanigaNFS",
    version="0.0.1",
    author="Jordan Milne",
    author_email="JordanMilne@users.noreply.github.com",
    description="Library for making somewhat conformant NFS and SunRPC clients and servers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/JordanMilne/ShenanigaNFS",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    extras_require={
        "rpcgen": ["ply~=3.11"],
    },
    python_requires='>=3.7',
)
