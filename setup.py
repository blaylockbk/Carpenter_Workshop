from pathlib import Path
from setuptools import setup, find_packages

HERE = Path(__file__).parent
README = (HERE / 'README.md').read_text(encoding="utf8")

setup(
    name = 'carpenter-workshop',
    version = '0.0.1',
    author = 'Brian K. Blaylock',
    author_email = "blaylockbk@gmail.com",
    description = "Brian's python workshop with tools, paint, and any other useful things.",
    long_description = README,
    long_description_content_type = 'text/markdown',
    project_urls = {
        'Source Code': 'https://github.com/blaylockbk/Carpenter_Workshop',
        'Documentation': 'https://blaylockbk.github.io/Carpenter_Workshop/_build/html/',
    },
    license = "MIT",
    packages = find_packages(),
    package_data = {
        "": ['*.cfg'],
    },
    install_requires = ['curl', 'numpy', 'pandas', 'xarray'],
    keywords = ['xarray', 'meteorology', 'weather', 'numerical weather prediction', 'forecast'],
    classifiers = [
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Intended Audience :: Developers",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering :: Atmospheric Science",
    ],
    zip_safe = False,
)

###############################################################################
## Brian's Note: How to upload a new version to PyPI
## -------------------------------------------------
# Created a new conda environment with twine
# conda create -n pypi python=3 twine pip -c conda-forge
'''
conda activate pypi
cd Carpenter_Workshop
python setup.py sdist bdist_wheel
twine check dist/*
# Test PyPI
twine upload --skip-existing --repository-url https://test.pypi.org/legacy/ dist/*
# PyPI
twine upload --skip-existing dist/*
'''