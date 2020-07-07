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
    #this_DEM.download()
    
    this_DEM.to_UTM_pythonic()


def test_02():
    
    # Now I am going to try to get a hillshade
    #rast = gio.ReadRasterArrayBlocks_numpy("mySRTM_SRTM30_UTM.tif")
    
    src =  rio.open("mySRTM_SRTM30_UTM.tif")
    rast = src.read(1)
    
    rast = rast.astype(float)
    rast[rast < -5] = np.nan
    
    hs_rast = lsdplt.Hillshade(rast)
    
    gio.array2raster("mySRTM_SRTM30_UTM.tif","mySRTM_SRTM30_UTM_HS.bil",hs_rast)
    gio.array2raster("mySRTM_SRTM30_UTM.tif","mySRTM_SRTM30_UTM.bil",rast)


    DataDirectory = "./"
    Base_file = "mySRTM_SRTM30_UTM"
    
    lsdmw.SimpleHillshade(DataDirectory,Base_file)


if __name__ == "__main__":
    test_02()
    #run_tests_2()
    