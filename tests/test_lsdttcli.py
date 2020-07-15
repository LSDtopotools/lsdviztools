#!/usr/bin/env python

'''
A script for testing the lsdttcli object
Simon Mudd
06/07/2020
'''

import lsdviztools.lsdmapwrappers as lsdmw
import os
import subprocess

def test_01():


    param_dict = {"write_hillshade" : "true",
                  "remove_seas" : "true",
                  "print_fill_raster" : "true",
                  "convert_csv_to_geojson" : "true",
                  "print_channels_to_csv": "true"}

    lsdtt_drive = lsdmw.lsdtt_driver(driver_name = "CLI_01", read_prefix = "CP_SRTM30_UTM",write_prefix= "CP_SRTM30_UTM",parameter_dictionary = param_dict)
    lsdtt_drive.print_parameters()

    lsdtt_drive.run_lsdtt_command_line_tool()



if __name__ == "__main__":
    test_01()
    #run_tests_2()
