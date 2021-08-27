#!/usr/bin/env python

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['numpy','pandas','rasterio','scipy','cartopy','fiona','shapely','geopandas','pyproj','gdal','utm','matplotlib']

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest>=3', ]

setup(
    author="Simon Marius Mudd",
    author_email='simon.m.mudd@ed.ac.uk',
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description="lsdviztools is a collection of routines for plotting geospatial data, with a focus on data produces by LSDTopoTools or by lsdtopytools.",
    entry_points={
        'console_scripts': [
            'lsdtt_plotbasicrasters=lsdviztools.scripts.lsdtt_plotbasicrasters:main',
            'lsdtt_plotconcavityanalysis=lsdviztools.scripts.lsdtt_plotconcavityanalysis:main',
            'lsdtt_plotchianalysis=lsdviztools.scripts.lsdtt_plotchianalysis:main',
            'lsdtt_grabopentopographydata=lsdviztools.scripts.lsdtt_grabopentopographydata:main'
        ],
    },
    install_requires=requirements,
    license="MIT license",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='lsdviztools,lsdtopotools,lsdtopytools,GIS,topographic analysis,remote sensing,geomorphology,earth observation',
    name='lsdviztools',
    packages=find_packages(include=['lsdviztools', 'lsdviztools.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/simon-m-mudd/lsdviztools',
    version='0.4.7',
    zip_safe=False,
)
