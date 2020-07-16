#!/usr/bin/env python

'''
A script for testing the some mapwrappers object
Simon Mudd
06/07/2020
'''

import lsdviztools.lsdmapwrappers as lsdmw

def test_01():
    fname_prefix = "CP_SRTM30_UTM"
    DataDirectory = "./"

    lsdmw.PrintAllChannels(DataDirectory,fname_prefix,cmap = "terrain", channel_colourmap = "Blues")

def test_02():
    Base_file = "CP_SRTM30_UTM"
    Drape_prefix = "CP_SRTM30_UTM_SLOPE"
    DataDirectory = "./"

    lsdmw.SimpleDrape(DataDirectory,Base_file, Drape_prefix,cmap = "viridis", cbar_loc = "right", cbar_label = "Slope (m/m)", size_format = "geomorphology", fig_format = "jpg", dpi = 600, out_fname_prefix = "slope_image", coord_type = "UTM_km", use_scalebar = True, colour_min_max = [0.2,1.5])

    Base_file = "CP_SRTM30_UTM"
    Drape_prefix = "CP_SRTM30_UTM_SLOPE"
    DataDirectory = "./"

    lsdmw.SimpleDrape(DataDirectory,Base_file, Drape_prefix,cmap = "Spectral", cbar_loc = "top", cbar_label = "curvature (1/m)", size_format = "geomorphology", fig_format = "jpg", dpi = 600, out_fname_prefix = "curv_image", coord_type = "UTM_km", use_scalebar = True, colour_min_max = [-0.4,0.4])

if __name__ == "__main__":
    #test_01()
    test_02()
