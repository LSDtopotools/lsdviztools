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
    
    
    #param_dict = {}
    
    lsdtt_drive = lsdmw.lsdtt_driver(read_prefix = "lg_conception_SRTM30_UTM",write_prefix= "lg_conception_SRTM30_UTM")
    lsdtt_drive.print_parameters()
      
    lsdtt_drive.run_lsdtt_command_line_tool()
    
    

if __name__ == "__main__":
    test_01()
    #run_tests_2()
    