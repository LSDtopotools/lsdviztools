=======
History
=======

0.1.0 (2020-05-01)
------------------

* First release on PyPI.

0.2.0 (2020-06-16)
------------------

* Minor bug fixes

0.3.0 (2020-09-03)
------------------

* Minor bug fixes

0.4.0 (2021-02-03)
------------------

* Updated opentopography API and fixed chi mapping interface

0.4.4 (2021-03-02)
------------------

* Fixed a bug in the projection section of gdalio. Trying to make the code more resistent to errors generate by different versions of proj


0.4.5 (2021-07-22)
------------------

This release of lsdviztools adds some command line scripts for plotting basic rasters, chi analysis and concavity analysis.
It also adds functionality for using the opentopography API, including downloading of data using the API key, so it includes, for example, the copernicus DEMs.
It also fixes a bug with gdal that made up a pull request.


0.4.6 (2021-07-23)
------------------

Minor update that includes changes to make sure scripts run.

The four scripts are

* lsdtt_plotbasicmetrics for basic plotting
* lsdtt_plotchianalysis for channel profile analysis and tectonic geomorphology
* lsdtt_plotconcavityanalysis for concavity analysis of river profiles
* lsdtt_grabopentopographydata for grabbing data from opentopography.org


0.4.7 (2021-08-27)
------------------

Some fixes

* For scripts a fix to make sure you have the correct directory without the -dir flag
* A fix to the opentopography api key
* An update to the opentopography scraper that allows lower lef and upper right corners to be easily copied from google maps

0.4.8 (2022-09-15)
------------------

Some fixes

* More fixes to the opentopography grabber
* This uses an api key in a file now
