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

0.4.9 (2022-12-13)
------------------

Some fixes

* Added the lsdtt-valley-metrics to the driver interface
* Added point mapping to the plotting tools
* A number of bug fixes to the command line interface


0.4.10 (2023-03-10)
-------------------

Some fixes

* Added the descartes dependency
* Small change to the swath plotting routine

0.4.11 (2023-03-27)
-------------------

Important fix

* Removed descartes dependency and switched this to a direct plotting routine. This fixes an error caused by transition to python 3.9 in google colab

0.4.12 (2024-02-09)
-------------------

* Trying to solve a weird problem with conversion to UTM
* Making hiding API key for opentopography
* Fixing another descartes problem

0.4.13 (2024-10-09)
-------------------

* Sorting out another hidden UTM issue. Ensures a single digit UTM is processed correctly.
* Sorting out another hidden UTM issue. Ensures a single digit UTM is processed correctly.
* Updated the list of datasets available from opentopography
* You can now download USGS data

0.4.14 (2024-11-22)
-------------------

* Slight adjustment to the csv ingestion in the rasterisation tools
* Updates to the basemaps. New functions to make and orthographic basemap and a large regional hillshade
* More flexibility in the points over hillshade function
* Added the scalebar option to a number of plot types

0.4.15 (2025-01-10)
-------------------
* Added function to plot line segments on a MapFigure object
* Added lsdtt-basin-metrics as allowed driver function
* Removed a depricated and unused import that threw an error
* New functions to download DEMs based on HydroBASINS outlines 