#!/usr/bin/env python

"""Tests for `lsdviztools` package."""

import pytest
import pandas as pd
import os
from lsdviztools import lsdmapwrappers as LSDMW


@pytest.fixture
def example_path():
    filepath = os.path.realpath(os.path.join(os.getcwd(),
                                             os.path.dirname(__file__)))
    shppath = os.path.join(filepath, 'fixtures/')
    return shppath

@pytest.fixture
def DoesBasinInfoExist(this_dir, fname_prefix):
    """
    This function checks to see if there is an AllBasinsInfo file, which is produced by the LSDTopoTools basin extraction routines in the chi_mapping_tool.
    
    Args: 
        DataDir (str): The name of the data directory
        fname_prefix (str): The prefix of the raster file to be analysed
        
    Returns:
        BasinInfoDF (pandas dataframe): The basin info in a pandas dataframe
        exising_basin_keys (int list): a list of integers with the basin keys
        
    Author: SMM
    
    Date 30/01/2017
    """
    # See if a basin info file exists and if so get the basin list
    print("Let me check if there is a basins info csv file.")
    BasinInfoPrefix = fname_prefix+"_AllBasinsInfo.csv"
    BasinInfoFileName = DataDir+BasinInfoPrefix
    existing_basin_keys = []
    DF = pd.DataFrame()
    
    if os.path.isfile(BasinInfoFileName): 
        print("There is a basins info csv file")
        BasinInfoDF = phelp.ReadBasinInfoCSV(DataDir, fname_prefix)
        existing_basin_keys = list(BasinInfoDF['basin_key'])
        existing_basin_keys = [int(x) for x in existing_basin_keys]
        DF=BasinInfoDF 
    else:
        print("I didn't find a basins info csv file. Check directory or filename.")
        
    return DF, existing_basin_keys


@pytest.fixture
def get_basin_keys():
    # Find the basin keys, if they exist
    
    these_bains_keys = []
    this_dir = example_path()
    fname_prefix = "Mega_divide"
    BasinInfoDF,existing_basin_keys = DoesBasinInfoExist(this_dir, fname_prefix)
    
    if len(existing_basin_keys) > 0:
        print("I've got some basin keys, they are: ")
        print(existing_basin_keys)
    
    # If the basin keys are not supplited then assume all basins are used. 
    if these_basin_keys == []:
        these_basin_keys = existing_basin_keys
        
    # Python is so amazing. Look at the line below.
    Mask_basin_keys = [i for i in existing_basin_keys if i not in these_basin_keys]
    print("All basins are: ")
    print(existing_basin_keys)
    print("The basins to keep are:")
    print(these_basin_keys)
    print("The basins to mask are:")
    print(Mask_basin_keys)    
    return BasinInfoDF,existing_basin_keys,these_basin_keys,Mask_basin_keys


@pytest.fixture
def simple_drape():
    """
    This tests the plot simple drape wrapper
    """
    this_dir = example_path()
    fname_prefix = "Mega_divide"
    drape_fname_prefix = "Mega_divide_hs"
    LSDMW.SimpleDrape(this_dir,fname_prefix, drape_fname_prefix)

@pytest.fixture
def categorised_drape():
    """
    This tests the plot simple drape wrapper
    """
    this_dir = example_path()
    fname_prefix = "Mega_divide"
    drape_fname_prefix = "Mega_divide_hs"
    LSDMW.PrintCategorised(this_dir,fname_prefix, drape_fname_prefix)
    
@pytest.fixture
def compex_basins():
    """
    This tests the plot simple drape wrapper
    """
    this_dir = example_path()
    fname_prefix = "Mega_divide"
    drape_fname_prefix = "Mega_divide_hs"
    BasinInfoDF,existing_basin_keys,these_basin_keys,Mask_basin_keys = get_basin_keys()
    LSDMW.PrintBasins_Complex(this_dir,fname_prefix,use_keys_not_junctions = True, show_colourbar = False,Remove_Basins = Mask_basin_keys)
    

    