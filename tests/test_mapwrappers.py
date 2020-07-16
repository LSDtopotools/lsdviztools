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



if __name__ == "__main__":
    test_01()
    #run_tests_2()
