#!/usr/bin/env python

'''
A script for testing the ot_scraper object
Simon Mudd
06/07/2020
'''

import lsdviztools.lsdbasemaptools as bmt
from lsdviztools.lsdplottingtools import lsdmap_gdalio as gio
import lsdviztools.lsdplottingtools as lsdplt
import rasterio as rio
import numpy as np
import lsdviztools.lsdmapwrappers as lsdmw

def test_01():
    this_DEM = bmt.ot_scraper()

    this_DEM.print_parameters()
    this_DEM.download_pythonic()

    this_DEM.to_UTM_pythonic()


def test_02():

    RasterFile = "CP_SRTM30_UTM.tif"
    DataDirectory = "./"

    gio.convert2bil(DataDirectory, RasterFile,minimum_elevation=0.1)

    gio.write_hillshade_bil(DataDirectory, RasterFile)


def test_03():
    SB_DEM = bmt.ot_scraper(source = "SRTM30",longitude_W = -120.464655, longitude_E = -120.254214, latitude_S = 34.440538, latitude_N = 34.610770,prefix = "CP")
    SB_DEM.print_parameters()

    SB_DEM.download_pythonic()
    SB_DEM.to_UTM_pythonic()


if __name__ == "__main__":
    test_03()
    test_02()
    #run_tests_2()
