#=============================================================================
# Script to plot some basic rasters
#
# Authors:
#     Simon Mudd, Boris Gailleton, Fiona J. Clubb
#=============================================================================
#=============================================================================
# IMPORT MODULES
#=============================================================================


#from __future__ import print_function
import sys
import os
import lsdviztools.lsdbasemaptools as bmt
from lsdviztools.lsdplottingtools import lsdmap_gdalio as gio

#=============================================================================
# This is just a welcome screen that is displayed if no arguments are provided.
#=============================================================================
def print_welcome():

    print("\n\n=======================================================================")
    print("Hello! I'm going to grab some data from opentopography.")
    print("You will need to tell me which directory to look in.")
    print("Use the -dir flag to define the working directory.")
    print("If you don't do this I will assume the data is in the same directory as this script.")
    print("You also need to tell me the prefix of the DEM you want to download")
    print("Use the -fname flag to designate a file prefix")
    print("For help type:")
    print("   lsdtt_grabopentopographydata -h\n")
    print("=======================================================================\n\n ")
   
    
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
    
        
    #===============================================================================
    # These are some arguments for potting rasters other than the defaults
    parser.add_argument("-source", "--source", type=str, default = "SRTMGL1", help="The dataset you want. Options are: SRTMGL3, SRTMGL1, AW3D30, SRTM15Plus, NASADEM, COP30, COP90.")
    parser.add_argument("-south", "--south", type=float, default = 56.57, help="The southern latitude of the DEM in WGS84.")
    parser.add_argument("-north", "--north", type=float, default = 56.72, help="The northern latitude of the DEM in WGS84.")
    parser.add_argument("-east", "--east", type=float, default = -4.89, help="The eastern latitude of the DEM in WGS84.")
    parser.add_argument("-west", "--west", type=float, default = -5.13, help="The western latitude of the DEM in WGS84.")
    parser.add_argument("-resolution", "--resolution", type=float, default = 30, help="The raster resolution. This is only used if you convert the DEM but don't download it. If you download it will use the downloaded resolution.")
   

    parser.add_argument("-api_key", "--api_key", type=str, default = "NULL", help="The api key from OpenTopography. You need to create an account and grab your own api key.")
    parser.add_argument("-convert_for_lsdtt", "--convert_for_lsdtt", type=bool, default = True, help="Converts the DEM to bil format for ingestion into lsdtt command line tools.")
    parser.add_argument("-download_dem", "--download_dem", type=bool, default = True, help="Downloads the DEM from opentopography.org.")
    parser.add_argument("-write_hillshade_bil", "--write_hillshade_bil", type=bool, default = True, help="Writes a hillshade bil file for plotting with plotbasicrasters.")

    args = parser.parse_args()

    if not args.fname_prefix:
        print("WARNING! You haven't supplied your DEM name. Please specify this with the flag '-fname'")
        sys.exit()

    # get the base directory
    if args.base_directory:
        this_dir = args.base_directory
        # check if you remembered a / at the end of your path_name
        if not this_dir.endswith(os.sep):
            print("You forgot the separator at the end of the directory, appending...")
            this_dir = this_dir+os.sep
    else:
        this_dir = os.getcwd()+os.sep


    print("Creating an opentopography scraper")
    YOUR_DEM_SCRAPER = bmt.ot_scraper(source = args.source,longitude_W = args.west, longitude_E = args.east,latitude_S = args.south, latitude_N = args.north,prefix = args.fname_prefix,path = this_dir)

    print("The scraper parameters are:")
    YOUR_DEM_SCRAPER.print_parameters()

    
    if args.download_dem:
        print("Grabbing the DEM from opentopography. This may take a moment")
        RasterFile,RasterPath,fwithoutpath = YOUR_DEM_SCRAPER.download_pythonic()

    
    if args.convert_for_lsdtt:
        print("Converting the raster to a format the lsdtopotools command line tools can understand")

        if args.download_dem:
            rasterres = YOUR_DEM_SCRAPER.resolution

            print("The path is: "+RasterPath+ " and the file is: "+ fwithoutpath + " resolution: "+str(rasterres))
            NewRasterName = gio.convert4lsdtt(RasterPath, fwithoutpath,minimum_elevation=0.01,resolution=rasterres)
        else:
            NewRasterName = gio.convert4lsdtt(this_dir, args.fname_prefix,minimum_elevation=0.01,resolution=args.resolution)


    if args.write_hillshade_bil:
        print("Writing a hillshade")

        if args.convert_for_lsdtt:
            print("The path is: "+RasterPath+ " and the file is: "+ NewRasterName)
            gio.write_hillshade_bil(RasterPath, NewRasterName)
        else:
            gio.write_hillshade_bil(this_dir, args.fname_prefix)



#=============================================================================
if __name__ == "__main__":
    main()

