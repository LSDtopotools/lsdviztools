#!/usr/bin/env python

'''
A script for testing the ot_scraper object
Simon Mudd
06/07/2020
'''

import lsdviztools.lsdbasemaptools as bmt


def test_01():
    this_DEM = bmt.ot_scraper()
    
    this_DEM.print_parameters()
    this_DEM.download_pythonic()
    #this_DEM.download()
    
    this_DEM.to_UTM_pythonic()









if __name__ == "__main__":
    test_01()
    #run_tests_2()
    