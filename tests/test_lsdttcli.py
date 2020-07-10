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
    
    lsdtt_drive = lsdmw.lsdtt_driver(read_prefix = "mySRTM_SRTM30_UTM")
    lsdtt_drive.print_parameters()
    
    lsdtt_drive.write_lsdtt_driver()
    
    

if __name__ == "__main__":
    test_01()
    #run_tests_2()
    