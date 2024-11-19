## LSDMap_BasemapTools.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
## These functions are tools to create a basemap
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
## SMM
## 24/01/2018
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#from __future__ import absolute_import, division, print_function, unicode_literals
from __future__ import absolute_import, division, print_function


import matplotlib
matplotlib.use('Agg')

import pyproj   # For some crazy reason you need to import this first or it throws an error.
import cartopy
import cartopy.crs as ccrs
import cartopy.feature as cfeature
#from cartopy.io.shapereader import Reader
from cartopy.feature import ShapelyFeature
import cartopy.io.shapereader as shpreader

from lsdviztools.lsdplottingtools import lsdmap_gdalio as LSDMGDAL
#from lsdplottingtools import lsdmap_gdalio as LSDMGDAL
#from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.cm
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
from matplotlib.colors import Normalize
import os
from cartopy.io.shapereader import Reader
from shapely.geometry import shape


def BasemapExtentSizer(FigWidthInches, FigHeightInches):
    """
    The returns the aspect ratio that you need for the main figure given the dimensions of the figure.
    Basically this just calculates the padding needed for the axis labels

    Args:
        FigWidthInches (float): How wide you want the basemap
        FigHeightInches (float): How high you want your basemap

    Returns: The aspect ratio (a float) of the basemap extent.
    Author: SMM

    Date 03/02/2018
    """

    x_width = FigWidthInches - 0.3  # The 0.3 inches is the text)
    y_width = FigHeightInches - 0.2

    aspect_ratio = x_width/y_width
    return aspect_ratio

def GenerateExtentShapefile(DataDirectory, RasterFile):
    """
    This just wraps a LSDMap_GDALIO script

    Args:
        DataDirectory (str): the data directory with the basin raster
        RasterFile (str): the name of the raster

    Returns:
        Shapefile of the raster footprint. Has "_footprint" in filename.

    Author: SMM

    Date: 24/01/2018

    """
    LSDMGDAL.CreateShapefileOfRasterFootprint(DataDirectory, RasterFile)

def GenerateBasemapImageOrthographic(DataDirectory, RasterFile, FigWidthInches = 1, FigHeightInches = 1, FigFormat = "png", fig_dpi = 500, out_fname_prefix = ""):
    """
    This makes an Orthographic basemap image. Uses data from the raster to size the figure and locate the centrepoint

    Args:
        DataDirectory (str): The directory of the raster file
        RasterFile (str): the name of the raster file (include extension)
        FigWidthInches (flt): How wide you want the basemap
        FigHeightInches (float): How high you want your basemap
        FigFormat (str): Figure format, can be `png`, `svg`, `pdf`, etc.
        fig_dpi (int): Dots per inch of your figure
        out_fname_prefix (str): The prefix of the image file. If blank uses the fname_prefix


    Author: SMM

    Date: 19/11/2024
    """  

    # Make sure data directory is in correct format
    if not DataDirectory.endswith(os.sep):
        print("You forgot the separator at the end of the directory, appending...")
        DataDirectory = DataDirectory+os.sep

    # Set up the figure. This is needed to both size the figure and get the axis handle for plotting polygons
    fig = plt.figure(figsize=(FigWidthInches, FigHeightInches))    
    
    # get some filenames
    RasterSplit = RasterFile.split(".")
    Raster_prefix = RasterSplit[0]
    Shape_name = DataDirectory+Raster_prefix+"_footprint.shp"
    SName = "Shape"

    # Get the name of the image
    if len(out_fname_prefix) == 0:
        FigFileName = DataDirectory+Raster_prefix+"_basemap."+FigFormat
    else:
        FigFileName = DataDirectory+out_fname_prefix+"_basemap."+FigFormat

    # Now we get the extents from the raster
    centre_lat, centre_long, extent_lat, extent_long, xproj_extent, yproj_extent = LSDMGDAL.GetCentreAndExtentOfRaster(DataDirectory, RasterFile)

    # Create an Orthographic projection centered on the given latitude and longitude
    ax = plt.axes(projection=ccrs.Orthographic(central_longitude=centre_long, central_latitude=centre_lat))

    # Add features to the map
    ax.add_feature(cfeature.LAND)
    ax.add_feature(cfeature.OCEAN)
    ax.add_feature(cfeature.COASTLINE,linewidth=0.25)
    #ax.add_feature(cfeature.BORDERS, linestyle=':')

    # Plot the given latitude and longitude
    ax.scatter(centre_long, centre_lat, marker='+', c='r', linewidth=0.5, s=0.5,transform=ccrs.Geodetic())
    ax.set_global()

    #A fancy arrow
    transform = ccrs.Orthographic()._as_mpl_transform(ax)
    ax.annotate('', xy=(centre_long, centre_lat), xytext=(centre_long, centre_lat-40),xycoords='data',size=10,arrowprops=dict(facecolor='red',ec = 'none',arrowstyle="fancy",connectionstyle="arc3,rad=-0.3"),transform=ccrs.Geodetic())   
  
    # Set the title
    #plt.title(f'Site midpoint: \n{centre_lat:.4f}, {centre_long:.4f}',fontsize=8)

    # Show the plot
    plt.savefig(FigFileName,format=FigFormat,dpi=fig_dpi)    

def GenerateBasemapImageAutomated(DataDirectory, RasterFile, FigWidthInches = 4, FigHeightInches = 3, FigFormat = "png", fig_dpi = 500, regional_extent_multiplier = 5, label_spacing_multiplier = 0.5, out_fname_prefix = "", is_orthographic = False):
    """
    This makes the basemap image. Uses data from the raster to size the figure and locate the centrepoint

    Args:
        DataDirectory (str): The directory of the raster file
        RasterFile (str): the name of the raster file (include extension)
        FigWidthInches (flt): How wide you want the basemap
        FigHeightInches (float): How high you want your basemap
        FigFormat (str): Figure format, can be `png`, `svg`, `pdf`, etc.
        fig_dpi (int): Dots per inch of your figure
        regional_extent_multiplier (float): How much bigger you want the extent vs the size of the raster
        label_spacing_multiplier (float): If the meridians and parallels are too close, increase this number. Default of 0.5
        out_fname_prefix (str): The prefix of the image file. If blank uses the fname_prefix


    Author: SMM

    Date: 01/02/2018
    """

    # Make sure data directory is in correct format
    if not DataDirectory.endswith(os.sep):
        print("You forgot the separator at the end of the directory, appending...")
        DataDirectory = DataDirectory+os.sep

    # Set up the figure. This is needed to both size the figure and get the axis handle for plotting polygons
    fig = plt.figure(figsize=(FigWidthInches, FigHeightInches))

    print("The size is: " +str(FigWidthInches)+", "+str(FigHeightInches))

    # get some filenames
    RasterSplit = RasterFile.split(".")
    Raster_prefix = RasterSplit[0]
    Shape_name = DataDirectory+Raster_prefix+"_footprint.shp"
    SName = "Shape"

    # Get the name of the image
    if len(out_fname_prefix) == 0:
        FigFileName = DataDirectory+Raster_prefix+"_basemap."+FigFormat
    else:
        FigFileName = DataDirectory+out_fname_prefix+"_basemap."+FigFormat

    # Now we get the extents from the raster
    centre_lat, centre_long, extent_lat, extent_long, xproj_extent, yproj_extent = LSDMGDAL.GetCentreAndExtentOfRaster(DataDirectory, RasterFile)


    aspect_ratio =  xproj_extent/yproj_extent
    
    # Figure out the longest dimension
    long_dimension = xproj_extent
    if yproj_extent > long_dimension:
        long_dimension = yproj_extent

    print("The long dimension is: "+str(long_dimension))

    # Get the full extent by mulitplying the longest extent by the multiplier
    full_dimension = long_dimension*regional_extent_multiplier


    # now get the two dimensions for the extent of the figure
    print("The aspect ratio is: "+str(aspect_ratio))
    if aspect_ratio > 1:
        # This is when the figure is wider than tall
        x_ext = full_dimension*aspect_ratio
        y_ext = full_dimension
        full_extent_long = extent_long*aspect_ratio*regional_extent_multiplier
        full_extent_lat = extent_long*regional_extent_multiplier
    else:
        x_ext = full_dimension
        y_ext = full_dimension*aspect_ratio
        full_extent_long = extent_lat*regional_extent_multiplier
        full_extent_lat = extent_lat*aspect_ratio*regional_extent_multiplier

    extents = [centre_long-0.5*full_extent_long,
                   centre_long+0.5*full_extent_long,
                   centre_lat-0.5*full_extent_lat,
                   centre_lat+0.5*full_extent_lat]

    print("Extents are: ")
    print(extents)


    if(is_orthographic):
        print("I am setting up an orthographic projection.")
        ax = fig.add_axes([0, 0, 1, 1], projection=ccrs.Orthographic(
                        central_latitude=centre_lat,
                        central_longitude=centre_long))

        ax.coastlines(resolution='110m',linewidth=0.5)
        borders_110m = cfeature.NaturalEarthFeature('cultural', 'admin_0_boundary_lines_land', '110m',edgecolor='face', facecolor=cfeature.COLORS['land'])
        ax.add_feature(borders_110m, edgecolor='black', facecolor = "none",linewidth=0.5)
        ax.gridlines()

    else:
        print("The projection is not orthographic.")
        
        # Create a projection for the map
        ax = plt.axes(projection=ccrs.PlateCarree())

        print("Setting extent.")
        ax.set_extent(extents, ccrs.PlateCarree())
        print("Finished setting extent.")

        land_50m = cfeature.NaturalEarthFeature('physical', 'land', '50m',
                                        edgecolor='face',
                                        facecolor=cfeature.COLORS['land'])
        borders_50m = cfeature.NaturalEarthFeature('cultural', 'admin_0_boundary_lines_land', '50m',
                                        edgecolor='face',
                                        facecolor=cfeature.COLORS['land'])
        ax.add_feature(land_50m, edgecolor='black', linewidth=0.5)
        ax.add_feature(borders_50m, edgecolor='black', facecolor = "none",linewidth=0.5)



    # create the shapefile
    print("Making the shapefile.")
    LSDMGDAL.CreateShapefileOfRasterFootprint(DataDirectory, RasterFile)

    shape_feature = cfeature.ShapelyFeature(Reader(Shape_name).geometries(), ccrs.PlateCarree(), edgecolor='black')
    ax.add_feature(shape_feature, facecolor='none',alpha=0.5, linewidth=0.5)


    ax.gridlines(draw_labels=False, dms=True, x_inline=False, y_inline=False)
    plt.savefig(FigFileName,format=FigFormat,dpi=fig_dpi)

