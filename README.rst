===============
lsdviztools
===============


.. image:: https://img.shields.io/pypi/v/lsdviztools.svg?branch=master
        :target: https://pypi.org/project/lsdviztools/

.. image:: https://travis-ci.com/LSDtopotools/lsdviztools.svg?branch=master
        :target: https://travis-ci.com/LSDtopotools/lsdviztools


lsdvizools is a collection of routines for plotting geospatial data, with a focus on data produced by LSDTopoTools or by lsdtopytools.


* Free software: MIT license
* Documentation: https://lsviztools.readthedocs.io.


Features
--------

* Plotting of rasters that includes formatting so you can get publication-ready figures with one command.
* Selection of basins and channels for topographic analysis.
* Tools for plotting point data, usually associated with channel networks, derived from LSDTopoTools command line tools.
* Downloading of data from opentopography,org


Examples
--------

Multiple examples can be found in the form of python notebooks located here: https://github.com/LSDtopotools/lsdtt_notebooks 

These notebooks can be opened using google colaboratory, only a functioning web browser is required. 

Getting started
---------------

You can install lsdviztools with pip.

You can also use our docker container (in the second command you need to change the path after -v to your local directory). You first need to install docker: https://www.docker.com/products/docker-desktop

::

  $ docker pull lsdtopotools/lsdtt_pytools_docker

  $ docker run -it -v /path/to/my/local/directory:/LSDTopoTools -p 8888:8888 lsdtopotools/lsdtt_pytools_docker

  # jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root

Then go to the jupyter notebook in your web browser by going to http://localhost:8888/




Credits
-------

This package was written by Simon M. Mudd, Fiona J. Clubb and Stuart W.D. Grieve

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
