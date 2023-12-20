from setuptools import find_packages, setup

from habr.career import __version__

with open("README.md", encoding="utf-8") as f:
    readme = f.read()

setup(
    author="Lysenko Vladimir",
    author_email="wofkin@gmail.com",
    python_requires=">=3.11",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Environment :: Console",
        "Environment :: Web Environment",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    description="Habr Career python client",
    install_requires=[
        "beautifulsoup4==4.12.2",
        "click==8.1.7",
        "parameterized==0.9.0",
        "requests==2.31.0",
        "pydantic==2.5.2",
        "rich==13.7.0",
    ],
    long_description=readme,
    keywords="habr_career,habr,career",
    name="Habr Career",
    packages=find_packages(include=["habr", "habr.*"]),
    url="https://github.com/0x55AAh/habr_career/",
    version=__version__,
    entry_points={
        "console_scripts": [
            "career = habr.career.cli:main",
        ],
    },
)
