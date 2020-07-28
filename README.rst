===============
lsdviztools
===============


.. image:: https://img.shields.io/pypi/v/lsdviztools.svg?branch=master
        :target: https://pypi.org/project/lsdviztools/

.. image:: https://travis-ci.com/LSDtopotools/lsdviztools.svg?branch=master
        :target: https://travis-ci.com/LSDtopotools/lsdviztools

.. image:: https://readthedocs.org/projects/lsdviztools/badge/?version=latest
        :target: https://lsdviztools.readthedocs.io/en/latest/?badge=latest
        :alt: Documentation Status


.. image:: https://pyup.io/repos/github/LSDtopotools/lsdviztools/shield.svg
     :target: https://pyup.io/repos/github/LSDtopotools/lsdviztools/
     :alt: Updates



lsdvizools is a collection of routines for plotting geospatial data, with a focus on data produced by LSDTopoTools or by lsdtopytools.


* Free software: MIT license
* Documentation: https://lsviztools.readthedocs.io.


Features
--------

* Plotting of rasters that includes formatting so you can get publication-ready figures with one command.
* Selection of basins and channels for topogroahic analysis.
* Tools for plotting point data, usually associated with channel networks, derived from LSDTopoTools command line tools.


Getting started
---------------

You can install lsdviztools with pip.

You can also use our docker container (in the second command you need to change the path after -v to your local directory). You first need to install docker: https://www.docker.com/products/docker-desktop

::
  $ docker pull lsdtopotools/lsdtt_pytools_docker
  $ docker run -it -v /path/to/my/local/directory:/LSDTopoTools -p 8888:8888 lsdtopotools/lsdtt_pytools_docker
  # install_lsdtt_python_packages.sh
  # jupyter notebook --ip 0.0.0.0 --port 8888 --no-browser --allow-root

Then go to the jupyter notebook in your web browser by going to http://localhost:8888/




Credits
-------

This package was created with Cookiecutter_ and the `audreyr/cookiecutter-pypackage`_ project template.

.. _Cookiecutter: https://github.com/audreyr/cookiecutter
.. _`audreyr/cookiecutter-pypackage`: https://github.com/audreyr/cookiecutter-pypackage
