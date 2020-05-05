#=============================================================================
# Script to plot some basic rasters
#
# Authors:
#     Simon Mudd, Boris Gailleton, Fiona J. Clubb
#=============================================================================
#=============================================================================
# IMPORT MODULES
#=============================================================================
# set backend to run on server
import matplotlib
matplotlib.use('Agg')

#from __future__ import print_function
import sys
import os
import pandas as pd
from lsdviztools.lsdplottingtools import lsdmap_movernplotting as MN
from lsdviztools import lsdmapwrappers as LSDMW
from lsdviztools.lsdmapfigure import plottinghelpers as phelp
import lsdviztools.lsdplottingtools as LSDP
from osgeo import ogr
#=============================================================================
# This is just a welcome screen that is displayed if no arguments are provided.
#=============================================================================
def print_welcome():

    print("\n\n=======================================================================")
    print("Hello! I'm going to plot some basic plots.")
    print("You will need to tell me which directory to look in.")
    print("Use the -dir flag to define the working directory.")
    print("If you don't do this I will assume the data is in the same directory as this script.")
    print("For help type:")
    print("   python PlotChiAnalysis.py -h\n")
    print("=======================================================================\n\n ")

    
#=============================================================================
# Some functions for managing directories
#=============================================================================     
def MakeRasterDirectory(this_dir):
    # check if a raster directory exists. If not then make it.
    raster_directory = this_dir+'raster_plots/'
    print("I am printing to a raster directory:")
    print(raster_directory)
    if not os.path.isdir(raster_directory):
        os.makedirs(raster_directory)  
        
#=============================================================================
# Some functions for managing directories
#=============================================================================     
def MakeBasemapDirectory(this_dir):
    # check if a raster directory exists. If not then make it.
    basemap_directory = this_dir+'basemap_plots/'
    print("I am printing to a raster directory:")
    print(basemap_directory)
    if not os.path.isdir(basemap_directory):
        os.makedirs(basemap_directory)    

#=============================================================================
# The normal float parsing doesn't work if on of the floats is 
# negative so I need to do this malarky -- SMM 2/03/2019
# see
# https://stackoverflow.com/questions/9025204/python-argparse-issue-with-optional-arguments-which-are-negative-numbers
#=============================================================================  
#def two_floats(value):
#    values = value.split()
#    if len(values) != 2:
#        raise argparse.ArgumentError
#    values = map(float, values)
#    return values       
        
#=============================================================================
# This parses a comma separated string
#=============================================================================    
def parse_list_from_string(a_string):
    """
    This just parses a comma separated string and returns an INTEGER or FLOAT list
    
    Args: 
        a_string (str): The string to be parsed
        
    Returns:
        A list of integers or floats. Floats if there is a decimal in the string
        
    Author: SMM
    
    Date: 10/01/2018
    """
    print("Hey pardner, I'm a gonna parse a string into a list. Yeehaw.")
    if len(a_string) == 0:
        print("No items found, I am returning and empty list.")
        return_list = []
    elif "." in a_string:
        print("I found a decimal in your string. I am going to assume these are floats")
        return_list = [float(item) for item in a_string.split(',')]
        print("The parsed string is:")
        print(return_list)
    else:
        return_list = [int(item) for item in a_string.split(',')]
        print("The parsed string is:")
        print(return_list)
        
    return return_list

#=============================================================================
# This parses a comma separated string of strongs
#=============================================================================    
def parse_string_list_from_string(a_string):
    """
    This just parses a comma separated string and returns an string list
    
    Args: 
        a_string (str): The string to be parsed
        
    Returns:
        A list of strings
        
    Author: SMM
    
    Date: 10/01/2018
    """
    print("Hey pardner, I'm a gonna parse a string into a list. Yeehaw.")
    if len(a_string) == 0:
        print("No items found, I am returning and empty list.")
        return_list = []
    else:
        return_list = a_string.split(',')
        print("The parsed string is:")
        print(return_list)
        
    return return_list


#=============================================================================
# This parses a dict separated string
#=============================================================================    
def parse_dict_from_string(a_string):
    """
    This takes a string that is formatted to create a dict. The format is that each key/value pair is separated by a "," and each key and value are separated with a ":"
    
    Args:
        a_string (int): The input string
        
    Returns: 
        A dictionary with the functions
        
    Author: SMM
        
    Date: 10/01/2018
    """
    if len(a_string) == 0:
        print("No rename dictionary found. I will return and empty dict.")
        this_rename_dict = {}
    else:
        listified_entry = [item for item in a_string.split(',')]
        this_rename_dict = {}
        
        # now loop through these creating a dict
        for entry in listified_entry:
            split_entry = entry.split(":")
            this_rename_dict[int(split_entry[0])]=split_entry[1]
    
    print("The parsed dict is: ")
    print(this_rename_dict)
    return this_rename_dict

#=============================================================================
# This parses a list of lists separated string. Each list is separated by a colon
#=============================================================================    
def parse_list_of_list_from_string(a_string):
    """
    This parses a list of lists separated string. Each list is separated by a colon
    
    Args:
        a_string (str): This creates a list of lists. Each sub list is separated by colons and the sub list items are separated by commas. So `1,2,3:4,5` would produce [ [1,2,3],[4,5]]
        
    Returns:
        list_of_list (list): A list of lists
        
    Author: SMM
    
    Date: 11/01/2018
    """
    
    if len(a_string) == 0:
        print("No list of list found. I will return an empty list.")
        list_of_list = []
    else:
        listified_entry = [item for item in a_string.split(':')]
        list_of_list = []
        
        # now loop through these creating a dict
        for entry in listified_entry:
            split_entry = [int(item) for item in entry.split(',')]
            list_of_list.append(split_entry)
    
    print("This list of lists is: ")
    print(list_of_list)
    
    return list_of_list

#=============================================================================
# This takes the basin stack list and then gives each basin in a stack layer
# a constant value. Used for plotting. 
#=============================================================================  
def convert_basin_stack_to_value_dict(basin_stack_list):
    """
    This takes the basin stack list and then gives each basin in a stack layer a constant value. Used for plotting. So if there are several basin stacks each one gets a different value. 
    
    Args:
        basin_stack_list (list of int lists): The basins that will be stacked. Each item in the list is a collection of basins that will be used in each indivdual stack plot. So, for example, if this is [ [1,2,3],[4,5]] then there will be two stacked plot, the first with basins 1,2,3 and the second with basins 4 and 5.
        
    Returns: 
        this_value_dict (dict): A dictionary assigning a single value to each basin. Basins in the same stack will have the same value. 
        
    Author: SMM
    
    Date: 11/01/2017
    
    """
    
    N_stacks = len(basin_stack_list)
    print("The number of stacks are: "+ str(N_stacks))
    if len(basin_stack_list) == 0:
        this_value_dict = {}
    else:
        this_value_dict = {}
        for idx,stack in enumerate(basin_stack_list):
            value = float(idx)/float(N_stacks)
            for item in stack:
                this_value_dict[item] = value
    return this_value_dict
                

#=============================================================================
# This pads an offset list so it is the same size as the basin list
#=============================================================================     
def pad_offset_lists(basin_stack_list,offset_list):
    """
    This pads an offset list so it is the same size as the basin list. The offsets are the coordinate distances between the starting node of adjacent profile plots.
    
    Args:
        basin_stack_list (list of int lists): The basins that will be stacked. Each item in the list is a collection of basins that will be used in each indivdual stack plot. So, for example, if this is [ [1,2,3],[4,5]] then there will be two stacked plot, the first with basins 1,2,3 and the second with basins 4 and 5. 
        offset_list (float list): A list of of the offset spacings for each basin stack.
        
    Return: 
        final_offsets (float list): The locations of the offsets.  
        
    Author: SMM
    
    Date: 09/01/2017
    """
    
    # I need to check chi the offsets
    n_basin_stacks = len(basin_stack_list)
    if len(offset_list) == 0:
        const_offset = 5
    else:
        const_offset = offset_list[-1]
    final_offsets = offset_list
    if len(offset_list) < n_basin_stacks:
        final_offsets = offset_list + [const_offset]*(n_basin_stacks - len(offset_list))
    else:
        final_offsets = offset_list

    print("Initial offsets are: ")
    print(offset_list)
    print("And const offset is: "+str(const_offset))
    print("Final offset is: ")
    print(final_offsets)
    
    return final_offsets
    
def DoesBasinInfoExist(DataDir,fname_prefix):
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
        
    
#=============================================================================
# This is the main function that runs the whole thing
#=============================================================================
def main(args=None):

    if args is None:
        args = sys.argv[1:]    
    
    # If there are no arguments, send to the welcome screen
    if not len(sys.argv) > 1:
        full_paramfile = print_welcome()
        sys.exit()

    # Get the arguments
    import argparse
    parser = argparse.ArgumentParser()
    
    #==========================================================================
    # The location of the data files
    parser.add_argument("-dir", "--base_directory", type=str, help="The base directory that contains your data files. If this isn't defined I'll assume it's the same as the current directory.")
    parser.add_argument("-fname", "--fname_prefix", type=str, help="The prefix of your DEM WITHOUT EXTENSION!!! This must be supplied or you will get an error (unless you're running the parallel plotting).")
    parser.add_argument("-out_fname", "--out_fname_prefix", type=str, help="The prefix of the figures WITHOUT EXTENSION!!! If not supplied the fname prefix will be used.")
    
    
    
    #===============================================================================
    # These are some arguments for potting rasters other than the defaults
    parser.add_argument("-drape_fname", "--drape_fname_prefix", type=str, help="The prefix of a raster that is used in a drape plot WITHOUT EXTENSION!!! If not supplied this will just use the hillshade.")
    parser.add_argument("-drape_cbar_loc", "--drape_cbar_loc", type=str, default = "right", help="This is the location of the colourbar for the drape plot. Options are None, left, right, top and bottom.")
    parser.add_argument("-drape_cbar_label", "--drape_cbar_label", type=str, default = "colourbar_label", help="This is the label on the colourbar.")
    parser.add_argument("-drape_cmap", "--drape_cmap", type=str, default = "jet", help="This is colourmap. See matplotlib docs for options.") 
    parser.add_argument("-drape_colour_min_max", "--drape_colour_min_max", default = "", help="Add a comma separated minimum and maximum colour for plotting. WARNING if one of the floats in negative you need to add a space before it in the string or else it will be treated as an option.") 

    
    #===============================================================================
    # These are some arguments for stacking plots
    parser.add_argument("-profile_stack_fnames", "--profile_stack_fnames", type=str, default = "", help="This is a comma separated list of file prefixes for stacking profile plots.")
   
    
    #===============================================================================
    # Selecting and renaming basins
    parser.add_argument("-basin_keys", "--basin_keys",type=str,default = "", help = "This is a comma delimited string that gets the list of basins you want for the plotting. Default = no basins")  
    parser.add_argument("-rename_dict", "--rename_dict",type=str,default = "", help = "This is a string that initiates a dictionary for renaming basins. The different dict entries should be comma separated, and key and value should be separated by a colon. Default = no dict")   
    parser.add_argument("-basin_lists", "--basin_lists",type=str,default = "", help = "This is a string that initiates a list of a list for grouping basins. The object becomes a list of a list but the syntax is comma seperated lists, and each one is separated by a colon. Default = no dict")
    parser.add_argument("-chi_offsets", "--chi_offsets",type=str,default = "", help = "This is a string that initiates a list of chi offsets for each of the basin lists. Default = no list")
    parser.add_argument("-fd_offsets", "--flow_distance_offsets",type=str,default = "", help = "This is a string that initiates a list of flow distance offsets for each of the basin lists. Default = no list")
    
    #===============================================================================    
    # What sort of analyses you want--these are rather simple versions
    parser.add_argument("-PB", "--plot_basins", type=bool, default=False, help="If this is true, I'll make a simple basin plot.")
    parser.add_argument("-PBC", "--plot_basins_channels", type=bool, default=False, help="If this is true, I'll make a simple basin plot with channels.")
    parser.add_argument("-PCh", "--plot_channels", type=bool, default=False, help="If this is true, I'll make a simple plot of channels.") 
    parser.add_argument("-PD", "--plot_drape", type=bool, default=False, help="If this is true, I'll make a simple draped plot that puts a colour scale on a drape of your choice.")
    parser.add_argument("-PC", "--plot_chi_coord", type=bool, default=False, help="If this is true, I'll make a chi coordinate plot.") 
    parser.add_argument("-SimpleChFmt", "--simple_channel_format", type=str, default="elevation", help="The column in the channel file used to colour the channels.")    
    parser.add_argument("-SStack", "--simple_stacked_plots", type=bool, default=False, help="Plots chi and  channel profile plots using only the chi data map csv.")  
    parser.add_argument("-MStack", "--multiple_stacked_plots", type=bool, default=False, help="Plots profiles from different files on top of one another.")  
    parser.add_argument("-PP", "--plot_points", type=bool, default=False, help="This plots points onto the map. You just need a lat-long file of points.")
    parser.add_argument("-PCat", "--plot_categorised", type=bool, default=False, help="This plots categorised data. Everything else works like a drape plot.")    
    
    #===============================================================================    
    # What sort of analyses you want--these are rather simple versions   
    parser.add_argument("-PS","--plot_swath", type=bool, default=False, help="If this is true, I'll plot a swath.")
    parser.add_argument("-swath_prefix","--swath_prefix", type=str, default="swath", help="This is the prefix to the swath filename.")
    
    #===============================================================================    
    # What sort of analyses you want--these lump different analyses
    parser.add_argument("-all", "--all_chi_plots", type=bool, default=False, help="If this is true, I'll make all the plots including raster and chi profile plots.")
    parser.add_argument("-all_rasters", "--all_raster_plots", type=bool, default=False, help="If this is true, I'll make all the raster plots.")
    parser.add_argument("-all_stacks", "--all_stacked_plots", type=bool, default=False, help="If this is true, I'll make all the stacked plots.")
    
    # Some simple geographic functions that can aid in plotting regional maps. They do things like create shapefile that
    # can then be used with basemap. We don't include the basemap functions since that is not in the LSDTT toolchain (but
    # might get included later)
    parser.add_argument("-RF", "--create_raster_footprint_shapefile",type=bool, default=False, help="If true, create a shapefile from the raster. Can be used with basemap to make regional maps")
    parser.add_argument("-BM", "--create_basemap_figure",type=bool, default=False, help="If true, create a basemap file")

    # These control the format of your figures
    parser.add_argument("-drape_colour_norm", "--drape_colour_norm", type=str, default='none', help="This allows the user to set the colour normalisation. The options are none (which is just linear), LogNorm, PowerNorm, and SymLogNorm. See https://matplotlib.org/gallery/userdemo/colormap_normalizations.html#sphx-glr-gallery-userdemo-colormap-normalizations-py for details. If these options (case sentitive) are not use it defaults to none.")    
    parser.add_argument("-coord_type", "--coord_type", type=str, default='UTM_km', help="The tick coordinate type. Options are UTM, UTM_km and None. UTM has ticks in metres. None should produce no tick marks.")
    parser.add_argument("-scalebar", "--use_scalebar", type=bool, default=False, help="A boolean that determines if you use a scalebar. This is currently only in operation for the simple drape plot.")    
    parser.add_argument("-fmt", "--FigFormat", type=str, default='png', help="Set the figure format for the plots. Default is png")
    parser.add_argument("-size", "--size_format", type=str, default='ESURF', help="Set the size format for the figure. Can be 'big' (16 inches wide), 'geomorphology' (6.25 inches wide), or 'ESURF' (4.92 inches wide) (defualt esurf).")
    parser.add_argument("-ar", "--figure_aspect_ratio", type=float, default=2, help="The aspect ratio of profile plots. Doesn't affect maps, whose aspect ratio is set by the size of the DEM.")
    parser.add_argument("-parallel", "--parallel", type=bool, default=False, help="If this is true I'll assume you ran the code in parallel and append all your CSVs together before plotting.")
    parser.add_argument("-dpi", "--dpi", type=int, default=250, help="The dots per inch of your figure.")
    parser.add_argument("-bmpsm", "--basemap_parallel_spacing_multiplier", type=float, default=0.5, help="Basemap parallel spacing multiplier. Increase if parallels are too close on your basemap.")
    parser.add_argument("-bmrem", "--basemap_regional_extent_multiplier", type=float, default=4, help="Basemap regional extent multiplier. The multiple of the size of the raster to make the basemap extent")
    parser.add_argument("-bmortho", "--basemap_orthographic", type=bool, default=False, help="If this is true the basemap creates an orthographic map, that is a globe.")   
    parser.add_argument("-bmwidth", "--basemap_width_inches", type=float, default=4, help="Basemap width in inches (since matplotlib is written by yanks).")
    parser.add_argument("-bmar", "--basemap_aspect_ratio", type=float, default=1, help="Basemap aspect ratio.")
   
    args = parser.parse_args()

    if not args.fname_prefix:
        if not args.parallel:
            print("WARNING! You haven't supplied your DEM name. Please specify this with the flag '-fname'")
            sys.exit()

    if not args.drape_fname_prefix:
        print("WARNING! You haven't supplied a drape DEM name. I will assume it is the same as the fname")
        args.drape_fname_prefix = args.fname_prefix          
            
    if not args.out_fname_prefix:
        print("You did not give me an out name prefix. I am using the raster prefix.")
        out_fname_prefix = args.fname_prefix
    else:
        print("I am going to use an fname prefix for the outfiles")
        out_fname_prefix = args.out_fname_prefix

    # get the base directory
    if args.base_directory:
        this_dir = args.base_directory
        # check if you remembered a / at the end of your path_name
        if not this_dir.endswith(os.sep):
            print("You forgot the separator at the end of the directory, appending...")
            this_dir = this_dir+os.sep
    else:
        this_dir = os.getcwd()

    # some formatting for the figures
    if args.FigFormat == "manuscipt_svg":
        print("You chose the manuscript svg option. This only works with the -ALL flag. For other flags it will default to simple svg")
        simple_format = "svg"
    elif args.FigFormat == "manuscript_png":
        print("You chose the manuscript png option. This only works with the -ALL flag. For other flags it will default to simple png")
        simple_format = "png"
    else:
        simple_format = args.FigFormat
         
        
        
    
    # This is for swath plotting
    if args.plot_swath:
        print("Let me print a swath profile.")
        swath_csv = this_dir+args.swath_prefix+".csv"
        fig_fname = this_dir+"test_swath.png"
        print("The swath file is: "+swath_csv)
        LSDP.PlotSwath(swath_csv, FigFileName = fig_fname,size_format = args.size_format, fig_format = simple_format)
        
    # See if you should create a shapefile of the raster footprint             
    if args.create_raster_footprint_shapefile:
        print("Let me create a shapefile of the raster footprint")
        
        driver_name = "ESRI shapefile"
        driver = ogr.GetDriverByName(driver_name)
        #print("Driver is: ")
        #print(driver)
        #print("Now I'll try it from LSDPlottingTools")     
        RasterFile = args.fname_prefix+".bil"
        LSDP.CreateShapefileOfRasterFootprint(this_dir, RasterFile)
        
    # See if you should create a basemap
    if args.create_basemap_figure:
        import LSDBasemapTools as LSDBM
        
        MakeBasemapDirectory(this_dir)
        RasterFile = args.fname_prefix+".bil"
        basemap_out_prefix = "/basemap_plots/"+out_fname_prefix
        
        # This gets the positioning
        centre_lat, centre_long, extent_lat, extent_long, xproj_extent, yproj_extent = LSDP.GetCentreAndExtentOfRaster(this_dir, RasterFile)
        
        FWI = args.basemap_width_inches
        FHI = FWI/(args.basemap_aspect_ratio)
        
        print("The basemap centrepoint is: "+str(centre_lat)+"," +str(centre_long))
        LSDBM.GenerateBasemapImageAutomated(this_dir, RasterFile, FigWidthInches = FWI, FigHeightInches = FHI, regional_extent_multiplier = args.basemap_regional_extent_multiplier, label_spacing_multiplier = args.basemap_parallel_spacing_multiplier, out_fname_prefix = basemap_out_prefix, fig_dpi = args.dpi, is_orthographic = args.basemap_orthographic)
        
          
    # Parse any lists, dicts, or list of lists from the arguments   
    these_basin_keys = parse_list_from_string(args.basin_keys)
    this_rename_dict = parse_dict_from_string(args.rename_dict)
    basin_stack_list = parse_list_of_list_from_string(args.basin_lists)
    chi_offset_list = parse_list_from_string(args.chi_offsets)
    fd_offset_list = parse_list_from_string(args.flow_distance_offsets)
    this_drape_colour_min_max = parse_list_from_string(args.drape_colour_min_max)
    profile_stack_files = parse_string_list_from_string(args.profile_stack_fnames)
    
    # Get the colour min and max
    #if (args.drape_colour_min_max[0] == -99.99 & args.drape_colour_min_max[1] == -99.99):
    #    this_drape_colour_min_max = []
    #else:
    #    this_drape_colour_min_max = args.drape_colour_min_max
    

    # Find the basin keys, if they exist
    BasinInfoDF,existing_basin_keys = DoesBasinInfoExist(this_dir, args.fname_prefix)
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
    
    # Look to see if there is a basin stack list. If there is, organise it so that we have different values in the
    # value dict
    if len(basin_stack_list) == 0:
        temp_stack = []
        temp_stack.append(these_basin_keys)
        this_value_dict = convert_basin_stack_to_value_dict(temp_stack)
    else:
        this_value_dict = convert_basin_stack_to_value_dict(basin_stack_list)
        
    # Now make sure all basins have a value dict value
    value_dict_single_basin = {}
    for basin in these_basin_keys:
        value_dict_single_basin[basin] = 1
        if basin not in this_value_dict:
            this_value_dict[basin] = 1
     
    #print("The value dict is:")
    #print(this_value_dict)
    
    # Now if there is a rename dict, replace the value dict values with the rename keys
    if len(this_rename_dict) != 0:
        #print("There is a rename dict. Let me adjust some values.")
        rename_value_dict = {}
        for key in this_value_dict:
            #print("Key is: "+str(key))
            if key in this_rename_dict:
                #print("I found a rename key in the value dict, changing to :"+ str(this_rename_dict[key]))
                rename_value_dict[this_rename_dict[key]] = this_value_dict[key]
            else:
                rename_value_dict[key] = this_value_dict[key]
        this_value_dict = rename_value_dict
    #print("The new value dict is: ")
    print(this_value_dict)
            

    # Set default offsets
    if len(chi_offset_list) == 0:
        chi_offset_list.append(5)
    if len(fd_offset_list) == 0:
        fd_offset_list.append(20000)
    
    #print("I am matching the offest list lengths to the number of basin stacks")    
    final_chi_offsets = pad_offset_lists(basin_stack_list,chi_offset_list)
    final_fd_offsets = pad_offset_lists(basin_stack_list,fd_offset_list)

    
    # This is the most basic draped plot. 
    if args.plot_drape:
        print("Let me print a drape plot for you.")
        print("The colour min and max are (if empty lis, just used min and max of data):")
        print(this_drape_colour_min_max)

        
        MakeRasterDirectory(this_dir)
        raster_out_prefix = "/raster_plots/"+out_fname_prefix
        LSDMW.SimpleDrape(this_dir,args.fname_prefix, args.drape_fname_prefix, cmap = args.drape_cmap, size_format = args.size_format,fig_format = simple_format, dpi = args.dpi, out_fname_prefix = raster_out_prefix, cbar_loc = args.drape_cbar_loc, cbar_label = args.drape_cbar_label, coord_type = args.coord_type, use_scalebar = args.use_scalebar, drape_cnorm = args.drape_colour_norm, colour_min_max = this_drape_colour_min_max)
        
 
    # This just plots the basins. Useful for checking on basin selection
    if args.plot_categorised:
        print("I am going to plot categorised data. You need to define a drape name.")
        
        # check if a raster directory exists. If not then make it.
        raster_directory = this_dir+'raster_plots/'
        print("I am printing to a raster directory:")
        print(raster_directory)
        if not os.path.isdir(raster_directory):
            os.makedirs(raster_directory)
        
        raster_out_prefix = "/raster_plots/"+out_fname_prefix      
        # Now for raster plots
        # First the basins, labeled:
        LSDMW.PrintCategorised(this_dir,args.fname_prefix, args.drape_fname_prefix, show_colourbar = False,cmap = "jet", size_format = args.size_format,fig_format = simple_format, dpi = args.dpi, out_fname_prefix = raster_out_prefix+"_cat", cbar_loc = args.drape_cbar_loc, cbar_label = args.drape_cbar_label)


    # This just plots the basins. Useful for checking on basin selection
    if args.plot_basins:
        print("I am only going to print basins.")
        
        # check if a raster directory exists. If not then make it.
        raster_directory = this_dir+'raster_plots/'
        print("I am printing to a raster directory:")
        print(raster_directory)
        if not os.path.isdir(raster_directory):
            os.makedirs(raster_directory)
        
        raster_out_prefix = "/raster_plots/"+out_fname_prefix      
        # Now for raster plots
        # First the basins, labeled:
        LSDMW.PrintBasins_Complex(this_dir,args.fname_prefix,use_keys_not_junctions = True, show_colourbar = False,Remove_Basins = Mask_basin_keys, Rename_Basins = this_rename_dict,cmap = "jet", size_format = args.size_format,fig_format = simple_format, dpi = args.dpi, out_fname_prefix = raster_out_prefix+"_basins")
      
    # This just plots the basins with the channels. Useful for checking on basin selection.
    if args.plot_basins_channels:
        print("I am going to print basins and channels.")
        
        # check if a raster directory exists. If not then make it.
        raster_directory = this_dir+'raster_plots/'
        print("I am printing to a raster directory:")
        print(raster_directory)
        if not os.path.isdir(raster_directory):
            os.makedirs(raster_directory)
        
        raster_out_prefix = "/raster_plots/"+out_fname_prefix 
        
        # Get the names of the relevant files
        ChannelFname = args.fname_prefix+"_chi_data_map.csv"
        
        # First the basins, with blue channels scaled by drainage area
        #LSDMW.PrintBasins_Complex(this_dir,args.fname_prefix,use_keys_not_junctions = True, show_colourbar = False,Remove_Basins = Mask_basin_keys, Rename_Basins = this_rename_dict,cmap = "jet", size_format = args.size_format,fig_format = simple_format, dpi = args.dpi, out_fname_prefix = raster_out_prefix+"_basinschannels",include_channels = True, label_basins = False)  
        
        if args.simple_channel_format == "elevation":
            # Now plot the channels coloured by the source number
            LSDMW.PrintChiChannelsAndBasins(this_dir, args.fname_prefix, ChannelFileName = ChannelFname, add_basin_labels = False, cmap = "Blues_r", cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,plotting_column="elevation", Basin_remove_list = Mask_basin_keys, Basin_rename_dict = this_rename_dict, value_dict = this_value_dict, out_fname_prefix = raster_out_prefix+"_BChElevation", discrete_colours = False, colour_log = False, show_basins = True)  
        elif args.simple_channel_format == "source_key":
            # Now plot the channels coloured by the source number
            LSDMW.PrintChiChannelsAndBasins(this_dir, args.fname_prefix, ChannelFileName = ChannelFname, add_basin_labels = False, cmap = "tab20b", cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,plotting_column="source_key", Basin_remove_list = Mask_basin_keys, Basin_rename_dict = this_rename_dict, value_dict = this_value_dict, out_fname_prefix = raster_out_prefix+"BSourceKey", discrete_colours = True, NColours = 20, colour_log = False, show_basins = True)
        elif args.simple_channel_format == "basin_key":
            # Now plot the channels coloured by the source number
            LSDMW.PrintChiChannelsAndBasins(this_dir, args.fname_prefix, ChannelFileName = ChannelFname, add_basin_labels = False, cmap = "jet", cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,plotting_column="source_key", Basin_remove_list = Mask_basin_keys, Basin_rename_dict = this_rename_dict, value_dict = this_value_dict, out_fname_prefix = raster_out_prefix+"BBasinKey", discrete_colours = True, NColours = 20, colour_log = False, show_basins = True)
        elif args.simple_channel_format == "drainage_area":
            # Now plot the channels coloured by the source number
            LSDMW.PrintChiChannelsAndBasins(this_dir, args.fname_prefix, ChannelFileName = ChannelFname, add_basin_labels = False, cmap = "Reds_r", cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,plotting_column="elevation", Basin_remove_list = Mask_basin_keys, Basin_rename_dict = this_rename_dict, value_dict = this_value_dict, out_fname_prefix = raster_out_prefix+"_BDrainArea", discrete_colours = False, colour_log = True, show_basins = True) 
        else:
            print("You didn't select a valid channel colouring scheme.\n Choices are elevation, source_key, basin_key, and drainage_area")

    # This just plots the basins with the channels. Useful for checking on basin selection.
    if args.plot_channels:
        print("I am going to print channels.")
        
        # check if a raster directory exists. If not then make it.
        raster_directory = this_dir+'raster_plots/'
        print("I am printing to a raster directory:")
        print(raster_directory)
        if not os.path.isdir(raster_directory):
            os.makedirs(raster_directory)
            
        # Get the names of the relevant files
        ChannelFname = args.fname_prefix+"_chi_data_map.csv"
        
        raster_out_prefix = "/raster_plots/"+out_fname_prefix   
        
        # First the basins, with blue channels scaled by drainage area
        # Now plot the channels coloured by the elevation
        if args.simple_channel_format == "elevation":
            # Now plot the channels coloured by the source number
            LSDMW.PrintChiChannelsAndBasins(this_dir, args.fname_prefix, ChannelFileName = ChannelFname, add_basin_labels = False, cmap = args.drape_cmap, cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,plotting_column="elevation", Basin_remove_list = Mask_basin_keys, Basin_rename_dict = this_rename_dict, value_dict = this_value_dict, out_fname_prefix = raster_out_prefix+"_ChElevation", discrete_colours = False, colour_log = False, show_basins = False)  
        elif args.simple_channel_format == "source_key":
            # Now plot the channels coloured by the source number
            LSDMW.PrintChiChannelsAndBasins(this_dir, args.fname_prefix, ChannelFileName = ChannelFname, add_basin_labels = False, cmap = args.drape_cmap, cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,plotting_column="source_key", Basin_remove_list = Mask_basin_keys, Basin_rename_dict = this_rename_dict, value_dict = this_value_dict, out_fname_prefix = raster_out_prefix+"SourceKey", discrete_colours = True, NColours = 20, colour_log = False, show_basins = False)
        elif args.simple_channel_format == "basin_key":
            # Now plot the channels coloured by the source number
            LSDMW.PrintChiChannelsAndBasins(this_dir, args.fname_prefix, ChannelFileName = ChannelFname, add_basin_labels = False, cmap = args.drape_cmap, cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,plotting_column="source_key", Basin_remove_list = Mask_basin_keys, Basin_rename_dict = this_rename_dict, value_dict = this_value_dict, out_fname_prefix = raster_out_prefix+"BasinKey", discrete_colours = True, NColours = 20, colour_log = False, show_basins = False)
        elif args.simple_channel_format == "drainage_area":
            # Now plot the channels coloured by the source number
            LSDMW.PrintChiChannelsAndBasins(this_dir, args.fname_prefix, ChannelFileName = ChannelFname, add_basin_labels = False, cmap = args.drape_cmap, cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,plotting_column="elevation", Basin_remove_list = Mask_basin_keys, Basin_rename_dict = this_rename_dict, value_dict = this_value_dict, out_fname_prefix = raster_out_prefix+"_DrainArea", discrete_colours = False, colour_log = True, show_basins = False) 
        else:
            print("You didn't select a valid channel colouring scheme.\n Choices are elevation, source_key, basin_key, and drainage_area")
                   
 

   # This just plots the basins with the channels. Useful for checking on basin selection.
    if args.plot_points:
        print("I am going to plot some points.")
        
        # check if a raster directory exists. If not then make it.
        raster_directory = this_dir+'raster_plots/'
        print("I am printing to a raster directory:")
        print(raster_directory)
        if not os.path.isdir(raster_directory):
            os.makedirs(raster_directory)
            
        # Get the names of the relevant files
        ChannelFname = args.fname_prefix+"_points.csv"
        
        raster_out_prefix = "/raster_plots/"+out_fname_prefix 
        
        # First the basins, with blue channels scaled by drainage area
        # Now plot the channels coloured by the elevation
        if args.simple_channel_format == "elevation":
            # Now plot the channels coloured by the source number
            LSDMW.PrintChannels(this_dir, args.fname_prefix, ChannelFname,add_basin_labels = False, cmap = "gist_earth", cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi, out_fname_prefix = "", plotting_column = "elevation" )
        elif args.simple_channel_format == "source_key":
            # Now plot the channels coloured by the source number
            LSDMW.PrintChannels(this_dir, args.fname_prefix, ChannelFname,add_basin_labels = False, cmap = "gist_earth", cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi, out_fname_prefix = "", plotting_column = "source_key" )
        elif args.simple_channel_format == "basin_key":
            # Now plot the channels coloured by the source number
            LSDMW.PrintChannels(this_dir, args.fname_prefix, ChannelFname,add_basin_labels = False, cmap = "gist_earth", cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi, out_fname_prefix = "", plotting_column = "basin_key" )
        elif args.simple_channel_format == "drainage_area":
            # Now plot the channels coloured by the source number
            LSDMW.PrintChannels(this_dir, args.fname_prefix, ChannelFname,add_basin_labels = False, cmap = "gist_earth", cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi, out_fname_prefix = "", plotting_column = "drainage_area" )
        elif args.simple_channel_format == "none":
            # Now plot the channels coloured by the source number
            LSDMW.PrintChannels(this_dir, args.fname_prefix, ChannelFname,add_basin_labels = False, cmap = "gist_earth", cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi, out_fname_prefix = "", plotting_column = "none" )
        else:
            print("You didn't select a valid channel colouring scheme.\n Choices are elevation, source_key, basin_key, and drainage_area")

            
            
            
            
            
    # This plots the chi coordinate. It plots three different versions. 
    # extension _CC_basins are the absins used in the chi plot
    # extension _CC_raster plots the chi raster
    # extension _CC_channels plots the channels
    if args.plot_chi_coord:
        print("I am only going to print basins.")

        # check if a raster directory exists. If not then make it.
        raster_directory = this_dir+'raster_plots/'
        if not os.path.isdir(raster_directory):
            os.makedirs(raster_directory)

        # Get the names of the relevant files
        ChannelFname = args.fname_prefix+"_chi_data_map.csv"

        raster_out_prefix = "/raster_plots/"+args.fname_prefix
        # Now for raster plots
        # First the basins, labeled:
        LSDMW.PrintBasins_Complex(this_dir,args.fname_prefix,use_keys_not_junctions = True, show_colourbar = False,Remove_Basins = Mask_basin_keys, Rename_Basins = this_rename_dict,cmap = "jet", size_format = args.size_format,fig_format = simple_format, dpi = args.dpi, out_fname_prefix = raster_out_prefix+"_CC_basins")

        # Then the chi plot for the rasters. Only call this if the masked raster exists
        masked_fname = this_dir+args.fname_prefix+"_MaskedChi.bil"
        print("\n\n\nThe filename of the chi raster is: "+masked_fname+ " I am checking if it exists.")
        import os.path as osp
        if osp.isfile(masked_fname):
            print("The chi raster exists. I'll drape the channels over the chi raster")
            LSDMW.PrintChiCoordChannelsAndBasins(this_dir,args.fname_prefix, ChannelFileName = ChannelFname, add_basin_labels = False, cmap = "cubehelix", cbar_loc = "top", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,plotting_column = "chi", colour_log = False, colorbarlabel = "$\chi$", Basin_remove_list = Mask_basin_keys, Basin_rename_dict = this_rename_dict , value_dict = this_value_dict, out_fname_prefix = raster_out_prefix+"_CC_raster", plot_chi_raster = True)
        else:
            print("The chi raster doesn't exist, I am skpping to the channel chi plots.")

        LSDMW.PrintChiCoordChannelsAndBasins(this_dir,args.fname_prefix, ChannelFileName = ChannelFname, add_basin_labels = False, cmap = "cubehelix", cbar_loc = "top", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,plotting_column = "chi", colour_log = False, colorbarlabel = "$\chi$", Basin_remove_list = Mask_basin_keys, Basin_rename_dict = this_rename_dict , value_dict = this_value_dict, out_fname_prefix = raster_out_prefix+"_CC_channels", plot_chi_raster = False)
        
    # This bundles a number of different analyses    
    if args.all_chi_plots:
        print("You have chosen to plot all raster and stacked plots.")
        args.all_raster_plots = True
        args.all_stacked_plots = True

    # make the plots depending on your choices
    if args.all_raster_plots:
        print("I am goint to print some raster plots for you.")
        
        # check if a raster directory exists. If not then make it.
        raster_directory = this_dir+'raster_plots/'
        if not os.path.isdir(raster_directory):
            os.makedirs(raster_directory)
          
        # Get the names of the relevant files
        ChannelFname = args.fname_prefix+"_MChiSegmented.csv"
        
        raster_out_prefix = "/raster_plots/"+out_fname_prefix
        
        # Now for raster plots
        # First the basins, labeled:
        LSDMW.PrintBasins_Complex(this_dir,args.fname_prefix,use_keys_not_junctions = True, show_colourbar = False,Remove_Basins = Mask_basin_keys, Rename_Basins = this_rename_dict,cmap = "jet", size_format = args.size_format,fig_format = simple_format, dpi = args.dpi, out_fname_prefix = raster_out_prefix+"_basins")
        
        # Basins colour coded
        print("The value dict is: ")
        print(this_value_dict)
        LSDMW.PrintBasins_Complex(this_dir,args.fname_prefix,use_keys_not_junctions = True, show_colourbar = False,Remove_Basins = Mask_basin_keys, Rename_Basins = this_rename_dict, Value_dict = this_value_dict, cmap = "gray", size_format = args.size_format,fig_format = simple_format, dpi = args.dpi, out_fname_prefix = raster_out_prefix+"_stack_basins")
        
        # Now the chi steepness
        LSDMW.PrintChiChannelsAndBasins(this_dir, args.fname_prefix, ChannelFileName = ChannelFname, add_basin_labels = False, cmap = "viridis", cbar_loc = "right", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,plotting_column="m_chi",colorbarlabel = "$\mathrm{log}_{10} \; \mathrm{of} \; k_{sn}$", Basin_remove_list = Mask_basin_keys, Basin_rename_dict = this_rename_dict, value_dict = value_dict_single_basin, out_fname_prefix = raster_out_prefix+"_ksn")
        
        # Now plot the channels coloured by the source number
        LSDMW.PrintChiChannelsAndBasins(this_dir, args.fname_prefix, ChannelFileName = ChannelFname, add_basin_labels = False, cmap = "tab20b", cbar_loc = "None", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,plotting_column="source_key", Basin_remove_list = Mask_basin_keys, Basin_rename_dict = this_rename_dict, value_dict = this_value_dict, out_fname_prefix = raster_out_prefix+"sources", discrete_colours = True, NColours = 20, colour_log = False)
  
    if args.simple_stacked_plots:
 
        # check if a chi profile directory exists. If not then make it.
        chi_profile_directory = this_dir+'chi_profile_plots/'
        if not os.path.isdir(chi_profile_directory):
            os.makedirs(chi_profile_directory)   

        # Get the names of the relevant files
        ChannelFname = args.fname_prefix+"_chi_data_map.csv"
        
        raster_out_prefix = "/raster_plots/"+args.fname_prefix       
        
        print("I am going to plot simple chi and channel profile plots for you.")
        cbl = "$\mathrm{log}_{10} \; \mathrm{of} \; k_{sn}$"  
        print("The basins to print are")
        print(basin_stack_list)
        
        i = 0
        for little_list in basin_stack_list:
            i = i+1
            this_prefix = "chi_profile_plots/SimpleStacked_"+str(i) 
            
            print("The offset is: ")
            print("chi: "+str(final_chi_offsets[i-1]) )
            print("flow distance: "+ str(final_fd_offsets[i-1]) )
            
            
            # This prints the chi profiles coloured by elevation
            LSDMW.PrintChiStacked(this_dir, args.fname_prefix, ChannelFname, cmap = "viridis", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,axis_data_name="chi",plot_data_name = "elevation", plotting_data_format = 'normal',colorbarlabel = "elevation (m)", cbar_loc = "bottom", Basin_select_list = little_list, Basin_rename_dict = this_rename_dict, out_fname_prefix = this_prefix+"_chi",X_offset = final_chi_offsets[i-1], figure_aspect_ratio = args.figure_aspect_ratio)
        
            # This prints channel profiles coloured by elevation
            LSDMW.PrintChiStacked(this_dir, args.fname_prefix, ChannelFname, cmap = "viridis", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,axis_data_name="flow_distance",plot_data_name = "elevation", plotting_data_format = 'normal', colorbarlabel = "elevation (m)", Basin_select_list = little_list, Basin_rename_dict = this_rename_dict, out_fname_prefix = this_prefix+"_FD", X_offset = final_fd_offsets[i-1], figure_aspect_ratio = args.figure_aspect_ratio)    

            # This prints the channel profiles coloured by source number
            LSDMW.PrintChiStacked(this_dir, args.fname_prefix, ChannelFname, cmap = "tab20b", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,axis_data_name="flow_distance",plot_data_name = "source_key", plotting_data_format = 'normal', colorbarlabel = cbl, cbar_loc = "None", discrete_colours = True, NColours = 20, Basin_select_list = little_list, Basin_rename_dict = this_rename_dict, out_fname_prefix = this_prefix+"_Sources", X_offset = final_fd_offsets[i-1], figure_aspect_ratio = args.figure_aspect_ratio)    

    if args.multiple_stacked_plots:
        
        print("I am going to stack some profile plots for you.")
        print("The list of profile files is: ")
        print(profile_stack_files)
        
       # check if a chi profile directory exists. If not then make it.
        chi_profile_directory = this_dir+'chi_profile_plots/'
        if not os.path.isdir(chi_profile_directory):
            os.makedirs(chi_profile_directory)   
            
        ChannelFnameList = []
        for file in profile_stack_files:
            ChannelFname = args.base_directory+"/"+file+"_chi_data_map.csv"
            ChannelFnameList.append(ChannelFname)
            
        print("Filenames are:")
        print(ChannelFnameList)
            

        # Get the names of the relevant files
        little_list = [0]
        this_prefix = "chi_profile_plots/MultiStacked_"
        # This prints the channel profiles coloured by source number
        LSDMW.PrintMultipleStacked(this_dir, args.fname_prefix, ChannelFnameList, cmap = "tab20b", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,axis_data_name="flow_distance",plotting_data_format = 'normal', colorbarlabel = cbl, cbar_loc = "None", discrete_colours = True, NColours = 20, Basin_select_list = little_list, Basin_rename_dict = this_rename_dict, out_fname_prefix = this_prefix+"_Sources", X_offset = 0, figure_aspect_ratio = args.figure_aspect_ratio)  
            
            
        
    
            
    if args.all_stacked_plots:
 
        # check if a chi profile directory exists. If not then make it.
        chi_profile_directory = this_dir+'chi_profile_plots/'
        if not os.path.isdir(chi_profile_directory):
            os.makedirs(chi_profile_directory)   

        # Get the names of the relevant files
        ChannelFname = args.fname_prefix+"_MChiSegmented.csv"
        
        raster_out_prefix = "/raster_plots/"+args.fname_prefix       
        
        print("I am going to plot some chi stacks for you.")
        cbl = "$\mathrm{log}_{10} \; \mathrm{of} \; k_{sn}$"  
        i = 0
        for little_list in basin_stack_list:
            i = i+1
            this_prefix = "chi_profile_plots/Stacked_"+str(i) 
            
            print("The offset is: ")
            print("chi: "+str(final_chi_offsets[i-1]) )
            print("flow distance: "+ str(final_fd_offsets[i-1]) )
            
            
            # This prints the chi profiles coloured by k_sn
            LSDMW.PrintChiStacked(this_dir, args.fname_prefix, ChannelFname, cmap = "viridis", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,axis_data_name="chi",plot_data_name = "m_chi",colorbarlabel = cbl, cbar_loc = "bottom", Basin_select_list = little_list, Basin_rename_dict = this_rename_dict, out_fname_prefix = this_prefix+"_chi",X_offset = final_chi_offsets[i-1], figure_aspect_ratio = args.figure_aspect_ratio)
        
            # This prints channel profiles coloured by k_sn
            LSDMW.PrintChiStacked(this_dir, args.fname_prefix, ChannelFname, cmap = "viridis", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,axis_data_name="flow_distance",plot_data_name = "m_chi", plotting_data_format = 'log', colorbarlabel = cbl, Basin_select_list = little_list, Basin_rename_dict = this_rename_dict, out_fname_prefix = this_prefix+"_FD", X_offset = final_fd_offsets[i-1], figure_aspect_ratio = args.figure_aspect_ratio)    

            # This prints the channel profiles coloured by source number
            LSDMW.PrintChiStacked(this_dir, args.fname_prefix, ChannelFname, cmap = "tab20b", size_format = args.size_format, fig_format = simple_format, dpi = args.dpi,axis_data_name="flow_distance",plot_data_name = "source_key", plotting_data_format = 'normal', colorbarlabel = cbl, cbar_loc = "None", discrete_colours = True, NColours = 20, Basin_select_list = little_list, Basin_rename_dict = this_rename_dict, out_fname_prefix = this_prefix+"_Sources", X_offset = final_fd_offsets[i-1], figure_aspect_ratio = args.figure_aspect_ratio)    


#=============================================================================
if __name__ == "__main__":
    main()

