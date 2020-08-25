"""
    This contains wrapper functions that simplify plotting raster
    and vector data for publication-ready figures.

    The documentation of the examples can be found here:
    https://lsdtopotools.github.io/LSDTopoTools_ChiMudd2014/

    Simon Mudd and Fiona Clubb, June 2017

    Released under GPL3


"""

import matplotlib
# Force matplotlib to not use any Xwindows backend.
matplotlib.use('Agg')



import matplotlib.pyplot as plt
import matplotlib
from matplotlib import rcParams


"""
    IMPORTANT: You must call this function from a lower level driectory
    where both LSDPlottingTools and LSDMapFigure are in the python path!

    That is, it will not work if you call it from outside the directory structure.

"""
from lsdviztools.lsdplottingtools import lsdmap_pointtools as LSDP
from lsdviztools.lsdplottingtools import lsdmap_vectortools as LSDV
from lsdviztools.lsdmapfigure.plottingraster import MapFigure
from lsdviztools.lsdmapfigure import plottinghelpers as PlotHelp
from lsdviztools.lsdplottingtools import lsdmap_chiplotting as LSDCP

def make_display_string(img_name, width=600):
    """
    This makes a simple markdown display string that you can use in ipython

    Args:
        img_name (str): name of the image file
        width (int): the width of the figure in pixels

    Returns:
        a string that can be passed to the ipython markdown display command
        use with
        from IPython.display import display, Markdown, Latex
        todisplay = make_display_string(img_name, width=600)
        display(Markdown(todisplay))

    Author: SMM

    Date 25/08/2020
    """

    todisplay = r"""<img src="%s" width=%i>"""%(img_name,img_width)
    return todisplay

def SimpleHillshade(DataDirectory,Base_file, cmap = "terrain", cbar_loc = "right", size_format = "ESURF", fig_format = "png", dpi = 250, out_fname_prefix = "",save_fig = True):
    """
    This function makes a shaded relief plot of the DEM.

    Args:
        DataDirectory (str): the data directory with the rasters
        Base_file (str): The prefix for the rasters
        cmap (str or colourmap): The colourmap to use for the plot
        cbar_loc (str): where you want the colourbar. Options are none, left, right, top and botton. The colourbar will be of the elevation.
                        If you want only a hillshade set to none and the cmap to "gray"
        size_format (str): Either geomorphology or big. Anything else gets you a 4.9 inch wide figure (standard ESURF size)
        fig_format (str): An image format. png, pdf, eps, svg all valid
        dpi (int): The dots per inch of the figure
        out_fname_prefix (str): The prefix of the image file. If blank uses the fname_prefix
        save_fig (bool): If true, saves the fig, else, returns the filename

    Returns:
        If save_fig is true, return a string with the name of the image (printed to file). If save_fig is false, returns the figure handle to the hillshade plot

    Author: FJC, SMM
    """
    # specify the figure size and format
    # set figure sizes based on format
    if size_format == "geomorphology":
        fig_size_inches = 6.25
    elif size_format == "big":
        fig_size_inches = 16
    else:
        fig_size_inches = 4.92126
    ax_style = "Normal"

    # Get the filenames you want
    BackgroundRasterName = Base_file+"_hs.bil"
    DrapeRasterName = Base_file+".bil"

    # clear the plot
    plt.clf()

    # set up the base image and the map
    MF = MapFigure(BackgroundRasterName, DataDirectory,coord_type="UTM_km",colourbar_location = cbar_loc)
    MF.add_drape_image(DrapeRasterName,DataDirectory,colourmap = cmap, alpha = 0.6, colorbarlabel = "Elevation (m)")

    # Save the image or return the figure handle
    if (save_fig):
        if len(out_fname_prefix) == 0:
            ImageName = DataDirectory+Base_file+"_hillshade."+fig_format
        else:
            ImageName = DataDirectory+out_fname_prefix+"_hillshade."+fig_format

        MF.save_fig(fig_width_inches = fig_size_inches, FigFileName = ImageName, FigFormat=fig_format, Fig_dpi = dpi, transparent=True)

        thing_to_return = ImageName
    else:

        fig = MF.save_fig(fig_width_inches = fig_size_inches, transparent=True, return_fig = True)
        thing_to_return = fig

    print("I'm returning:")
    print(thing_to_return)
    return thing_to_return


def SimpleDrape(DataDirectory,Base_file, Drape_prefix, cmap = "cubehelix", cbar_loc = "right", cbar_label = "drape colourbar", size_format = "ESURF", fig_format = "png", dpi = 250, out_fname_prefix = "", coord_type = "UTM_km", use_scalebar = False, drape_cnorm = "none", colour_min_max = [],discrete_cmap=False, n_colours=10, save_fig = True):
    """
    This function makes a simple drape plot. You can choose the colourbar in this one. Similar to the PlotHillshade routine but a bit more flexible.

    Args:
        DataDirectory (str): the data directory with the rasters
        Base_file (str): The prefix for the rasters
        Drape_prefix (str): The prefix of the drape name
        cmap (str or colourmap): The colourmap to use for the plot
        cbar_loc (str): where you want the colourbar. Options are none, left, right, top and botton. The colourbar will be of the elevation.
                        If you want only a hillshade set to none and the cmap to "gray"
        cbar_label (str): The text on the colourbar label
        size_format (str): Either geomorphology or big. Anything else gets you a 4.9 inch wide figure (standard ESURF size)
        fig_format (str): An image format. png, pdf, eps, svg all valid
        dpi (int): The dots per inch of the figure
        out_fname_prefix (str): The prefix of the image file. If blank uses the fname_prefix
        coord_type (str): this can be in UTM_km or UTM_m
        use_scalebar (bool): If true inserts a scalebar in the image
        drape_cnorm (str): Sets the normalisation of the colourbar.
        colour_min_max (float list): Sets the minimum and maximum values of the colourbar
        discrete_cmap (bool): If true, make discrete values for colours, otherwise a gradient.
        n_colours (int): number of colours in discrete colourbar
        save_fig (bool): If true, saves the fig, else, returns the filename

    Returns:
        If save_fig is true, return a string with the name of the image (printed to file). If save_fig is false, returns the figure handle to the draped plot

    Author: FJC, SMM
    """
    # specify the figure size and format
    # set figure sizes based on format
    if size_format == "geomorphology":
        fig_size_inches = 6.25
    elif size_format == "big":
        fig_size_inches = 16
    else:
        fig_size_inches = 4.92126
    ax_style = "Normal"

    # Get the filenames you want
    BackgroundRasterName = Base_file+"_hs.bil"
    ElevationName = Base_file+".bil"
    DrapeName = Drape_prefix+".bil"

    # clear the plot
    plt.clf()

    # set up the base image and the map
    MF = MapFigure(BackgroundRasterName, DataDirectory,coord_type=coord_type,colourbar_location = cbar_loc)
    #MF.add_drape_image(ElevationName,DataDirectory,colourmap = "gray", alpha = 0.6, colorbarlabel = None)
    MF.add_drape_image(DrapeName,DataDirectory,colourmap = cmap, alpha = 0.6, colorbarlabel = cbar_label, norm = drape_cnorm, colour_min_max = colour_min_max,discrete_cmap = discrete_cmap,n_colours=n_colours)

    if(use_scalebar):
        print("Let me add a scalebar")
        MF.add_scalebar()

    # Save the image or return the figure handle
    if (save_fig):
        if len(out_fname_prefix) == 0:
            ImageName = DataDirectory+Base_file+"_drape."+fig_format
        else:
            ImageName = DataDirectory+out_fname_prefix+"_drape."+fig_format

        MF.save_fig(fig_width_inches = fig_size_inches, FigFileName = ImageName, FigFormat=fig_format, Fig_dpi = dpi, transparent=True)

        thing_to_return = ImageName
    else:
        fig = MF.save_fig(fig_width_inches = fig_size_inches, transparent=True, return_fig = True)
        thing_to_return = fig

    print("I'm returning:")
    print(thing_to_return)
    return thing_to_return


def SimpleHillshadeForAnimation(DataDirectory,Base_file, cmap = "jet", cbar_loc = "right",
                                size_format = "ESURF", fig_format = "png",
                                dpi = 250, imgnumber = 0, full_basefile = [],
                                custom_cbar_min_max = [], out_fname_prefix = "", coord_type="UTM_km", hide_ticklabels=False, save_fig = True):
    """
    This function make a hillshade image that is optimised for creating
    an animation. Used with the MuddPILE model

    Args:
        DataDirectory (str): the data directory with the data files
        Base_file (str): The prefix for the data files
        cmap (str or colourmap): The colourmap to use for the plot
        cbar_loc (str): where you want the colourbar. Options are none, left, right, top and botton. The colourbar will be of the elevation.
                        If you want only a hillshade set to none and the cmap to "gray"
        size_format (str): Either geomorphology or big. Anything else gets you a 4.9 inch wide figure (standard ESURF size)
        fig_format (str): An image format. png, pdf, eps, svg all valid
        dpi (int): The dots per inch of the figure
        imgnumber (int): the number of the image. Usually frames from model runs have integer numbers after them
        full_basefile (str): The root name of the figures you want. If empty, it uses the data_directory+base_file
        custom_min_max (list of int/float): if it contains two elements, recast the raster to [min,max] values for display.
        out_fname_prefix (str): The prefix of the image file. If blank uses the fname_prefix
        coord_type (str): either UTM or UTM_km
        hide_ticklabels (bool): if true, hide the tick labels from the plot

    Returns:
        A string with the name of the image (printed to file): Shaded relief plot. The elevation is also included in the plot.

    Author: FJC, SMM
    """
    # specify the figure size and format
    # set figure sizes based on format
    if size_format == "geomorphology":
        fig_size_inches = 6.25
    elif size_format == "big":
        fig_size_inches = 16
    else:
        fig_size_inches = 4.92126
    ax_style = "Normal"

    # Get the filenames you want
    BackgroundRasterName = Base_file+"_hs.bil"
    DrapeRasterName = Base_file+".bil"

    # clear the plot
    plt.clf()

    # set up the base image and the map
    MF = MapFigure(BackgroundRasterName, DataDirectory,coord_type=coord_type,colourbar_location = cbar_loc)
    MF.add_drape_image(DrapeRasterName,DataDirectory,colourmap = cmap, alpha = 0.6, colorbarlabel = "Elevation (m)",colour_min_max = custom_cbar_min_max)

    # Save the image
    if(full_basefile == []):
        if len(out_fname_prefix) == 0:
            ImageName = DataDirectory+Base_file+"_img"+"%004d" % (imgnumber)+"."+fig_format
        else:
            ImageName = DataDirectory+out_fname_prefix+"_img"+"%004d" % (imgnumber)+"."+fig_format
    else:
        ImageName = full_basefile+"_img"+"%004d" % (imgnumber)+"."+fig_format

    MF.save_fig(fig_width_inches = fig_size_inches, FigFileName = ImageName, axis_style = ax_style, FigFormat=fig_format, Fig_dpi = dpi, adjust_cbar_characters=False,
                 fixed_cbar_characters=4, hide_ticklabels=hide_ticklabels)
    return ImageName


def PrintAllChannels(DataDirectory,fname_prefix, add_basin_labels = True, cmap = "jet", cbar_loc = "right", size_format = "ESURF", fig_format = "png", dpi = 250, out_fname_prefix = "", channel_colourmap = "Blues", save_fig = True):
    """
    This function prints a channel map over a hillshade. It gets ALL the channels within the DEM: it automatically selects the _CN csv file that is obtained by the print channel network tool in lsdtopotools. Channels are coloured by the stream order.

    Args:
        DataDirectory (str): the data directory with the m/n csv files
        fname_prefix (str): The prefix for the m/n csv files
        add_basin_labels (bool): If true, label the basins with text. Otherwise use a colourbar.
        cmap (str or colourmap): The colourmap to use for the plot
        cbar_lox (str): where you want the colourbar. Options are none, left, right, top and botton. The colourbar will be of the elevation.
                        If you want only a hillshade set to none and the cmap to "gray"
        size_format (str): Either geomorphology or big. Anything else gets you a 4.9 inch wide figure (standard ESURF size)
        fig_format (str): An image format. png, pdf, eps, svg all valid
        dpi (int): The dots per inch of the figure
        out_fname_prefix (str): The prefix of the image file. If blank uses the fname_prefix
        channel_colourmap (str or cmap): the colourmap of the point data
        save_fig (bool): If true, saves the fig, else, returns the filename

    Returns:
        If save_fig is true, return a string with the name of the image (printed to file). If save_fig is false, returns the figure handle to the shaded relief plot with the channels.


    Author: SMM
    """
    # specify the figure size and format
    # set figure sizes based on format
    if size_format == "geomorphology":
        fig_size_inches = 6.25
    elif size_format == "big":
        fig_size_inches = 16
    else:
        fig_size_inches = 4.92126
    ax_style = "Normal"

    # Get the filenames you want
    BackgroundRasterName = fname_prefix+"_hs.bil"
    DrapeRasterName = fname_prefix+".bil"
    ChannelFileName = fname_prefix+"_CN.csv"
    chi_csv_fname = DataDirectory+ChannelFileName

    thisPointData = LSDP.LSDMap_PointData(chi_csv_fname)


    # clear the plot
    plt.clf()

    # set up the base image and the map
    MF = MapFigure(BackgroundRasterName, DataDirectory,coord_type="UTM_km",colourbar_location = "None")
    MF.add_drape_image(DrapeRasterName,DataDirectory,colourmap = cmap, alpha = 0.6)
    MF.add_point_data(thisPointData,column_for_plotting = "Stream Order", this_colourmap = channel_colourmap,
                       scale_points = True,column_for_scaling = "Stream Order",
                       scaled_data_in_log = False,
                       max_point_size = 5, min_point_size = 1,zorder = 10, alpha = 1)


    # Save the image
    thing_to_return = []
    if (save_fig):
        if len(out_fname_prefix) == 0:
            ImageName = DataDirectory+fname_prefix+"_channels."+fig_format
        else:
            ImageName = DataDirectory+out_fname_prefix+"_channels."+fig_format

        MF.save_fig(fig_width_inches = fig_size_inches, FigFileName = ImageName, FigFormat=fig_format, Fig_dpi = dpi, transparent=True)

        thing_to_return = ImageName

    else:
        fig = MF.save_fig(fig_width_inches = fig_size_inches, transparent=True, return_fig = True)
        thing_to_return = fig

    print("I'm returning:")
    print(thing_to_return)
    return thing_to_return


def PrintChannels(DataDirectory,fname_prefix, ChannelFileName, cmap = "jet", size_format = "ESURF", fig_format = "png", dpi = 250, out_fname_prefix = "", plotting_column = "basin_key", save_fig = True):
    """
    This function prints a channel map over a hillshade. It is more flexible than PrintAllChannels since you can choose the channel csv and you can also choose the column in the csv to plot

    Args:
        DataDirectory (str): the data directory with the m/n csv files
        fname_prefix (str): The prefix for the m/n csv files
        ChannelFileName (str): The name of the channel file. Doesn't need path but needs extension
        cmap (str or colourmap): The colourmap to use for the plot
        size_format (str): Either geomorphology or big. Anything else gets you a 4.9 inch wide figure (standard ESURF size)
        fig_format (str): An image format. png, pdf, eps, svg all valid
        dpi (int): The dots per inch of the figure
        out_fname_prefix (str): The prefix of the image file. If blank uses the fname_prefix
        plotting_column (str): the column to plot from the csv file
        save_fig (bool): If true, saves the fig, else, returns the filename

    Returns:
        If save_fig is true, return a string with the name of the image (printed to file). If save_fig is false, returns the figure handle to the shaded relief plot with the channels.

    Returns:
        A string with the name of the image (printed to file): A string with the name of the image (printed to file): Shaded relief plot with the basins coloured by basin ID. Uses a colourbar to show each basin

    Author: SMM
    """
    # specify the figure size and format
    # set figure sizes based on format
    if size_format == "geomorphology":
        fig_size_inches = 6.25
    elif size_format == "big":
        fig_size_inches = 16
    else:
        fig_size_inches = 4.92126
    ax_style = "Normal"

    # Get the filenames you want
    BackgroundRasterName = fname_prefix+"_hs.bil"
    DrapeRasterName = fname_prefix+".bil"
    chi_csv_fname = DataDirectory+ChannelFileName

    print("Let me get the point data")
    print("The filename is: "+chi_csv_fname)
    thisPointData = LSDP.LSDMap_PointData(chi_csv_fname)
    print("The parameter names are")
    thisPointData.GetParameterNames(True)



    # clear the plot
    plt.clf()

    # set up the base image and the map
    MF = MapFigure(BackgroundRasterName, DataDirectory,coord_type="UTM_km",colourbar_location = "None")
    MF.add_drape_image(DrapeRasterName,DataDirectory,colourmap = "gray", alpha = 0.6)
    MF.add_point_data(thisPointData,column_for_plotting = plotting_column,
                       scale_points = True, column_for_scaling = "drainage_area",
                       this_colourmap = cmap, scaled_data_in_log = True,
                       max_point_size = 5, min_point_size = 1)

    # Save the image
    thing_to_return = []
    if (save_fig):
        if len(out_fname_prefix) == 0:
            ImageName = DataDirectory+fname_prefix+"_channels_coloured_by_basin."+fig_format
        else:
            ImageName = DataDirectory+out_fname_prefix+"_channels_coloured_by_basin."+fig_format

        MF.save_fig(fig_width_inches = fig_size_inches, FigFileName = ImageName, FigFormat=fig_format, Fig_dpi = dpi, transparent=True)

        thing_to_return = ImageName

    else:
        fig = MF.save_fig(fig_width_inches = fig_size_inches, transparent=True, return_fig = True)
        thing_to_return = fig

    print("I'm returning:")
    print(thing_to_return)
    return thing_to_return




def PrintChannelsAndBasins(DataDirectory,fname_prefix, add_basin_labels = True, cmap = "jet", size_format = "ESURF", fig_format = "png", dpi = 250, out_fname_prefix = "", save_fig = True):
    """
    This function prints a channel map over a hillshade.

    Args:
        DataDirectory (str): the data directory with the m/n csv files
        fname_prefix (str): The prefix for the m/n csv files
        add_basin_labels (bool): If true, label the basins with text. Otherwise use a colourbar.
        cmap (str or colourmap): The colourmap to use for the plot
        size_format (str): Either geomorphology or big. Anything else gets you a 4.9 inch wide figure (standard ESURF size)
        fig_format (str): An image format. png, pdf, eps, svg all valid
        dpi (int): The dots per inch of the figure
        out_fname_prefix (str): The prefix of the image file. If blank uses the fname_prefix


    Returns:
        A string with the name of the image (printed to file): Shaded relief plot with the basins coloured by basin ID. Uses a colourbar to show each basin

    Author: SMM
    """
    # specify the figure size and format
    # set figure sizes based on format
    if size_format == "geomorphology":
        fig_size_inches = 6.25
    elif size_format == "big":
        fig_size_inches = 16
    else:
        fig_size_inches = 4.92126
    ax_style = "Normal"

    # get the basin IDs to make a discrete colourmap for each ID
    BasinInfoDF = PlotHelp.ReadBasinInfoCSV(DataDirectory, fname_prefix)

    basin_keys = list(BasinInfoDF['basin_key'])
    basin_keys = [int(x) for x in basin_keys]

    basin_junctions = list(BasinInfoDF['outlet_junction'])
    basin_junctions = [float(x) for x in basin_junctions]

    print ('Basin keys are: ')
    print (basin_keys)

    # going to make the basin plots - need to have bil extensions.
    print("I'm going to make the basin plots. Your topographic data must be in ENVI bil format or I'll break!!")

    # get the rasters
    raster_ext = '.bil'
    #BackgroundRasterName = fname_prefix+raster_ext
    HillshadeName = fname_prefix+'_hs'+raster_ext
    BasinsName = fname_prefix+'_AllBasins'+raster_ext
    print (BasinsName)
    Basins = LSDV.GetBasinOutlines(DataDirectory, BasinsName)


    ChannelFileName = fname_prefix+"_chi_data_map.csv"
    chi_csv_fname = DataDirectory+ChannelFileName

    thisPointData = LSDP.LSDMap_PointData(chi_csv_fname)

    # clear the plot
    plt.clf()

    # set up the base image and the map
    print("I am showing the basins without text labels.")
    MF = MapFigure(HillshadeName, DataDirectory,coord_type="UTM_km", colourbar_location="None")
    MF.plot_polygon_outlines(Basins, linewidth=0.8)
    MF.add_drape_image(BasinsName, DataDirectory, colourmap = cmap, alpha = 0.1, discrete_cmap=False, n_colours=len(basin_keys), show_colourbar = False, modify_raster_values=True, old_values=basin_junctions, new_values=basin_keys, cbar_type = int)

    MF.add_point_data(thisPointData,column_for_plotting = "basin_key",
                       scale_points = True,column_for_scaling = "drainage_area",
                       this_colourmap = cmap, scaled_data_in_log = True,
                       max_point_size = 3, min_point_size = 1)

    # Save the image
    thing_to_return = []
    if (save_fig):
        if len(out_fname_prefix) == 0:
            ImageName = DataDirectory+fname_prefix+"_channels_with_basins."+fig_format
        else:
            ImageName = DataDirectory+out_fname_prefix+"_channels_with_basins."+fig_format

        MF.save_fig(fig_width_inches = fig_size_inches, FigFileName = ImageName, FigFormat=fig_format, Fig_dpi = dpi, transparent=True)

        thing_to_return = ImageName

    else:
        fig = MF.save_fig(fig_width_inches = fig_size_inches, transparent=True, return_fig = True)
        thing_to_return = fig

    print("I'm returning:")
    print(thing_to_return)
    return thing_to_return


def PrintBasins(DataDirectory,fname_prefix, add_basin_labels = True, cmap = "jet", cbar_loc = "right", size_format = "ESURF", fig_format = "png", dpi = 250, out_fname_prefix = ""):
    """
    This function makes a shaded relief plot of the DEM with the basins coloured
    by the basin ID.

    IMPORTANT: To get this to run you need to set the flags in chi mapping tool to:
    write_hillshade: true
    print_basin_raster: true
    print_chi_data_maps: true

    Args:
        DataDirectory (str): the data directory with the m/n csv files
        fname_prefix (str): The prefix for the m/n csv files
        add_basin_labels (bool): If true, label the basins with text. Otherwise use a colourbar.
        cmap (str or colourmap): The colourmap to use for the plot
        cbar_loc (str): where you want the colourbar. Options are none, left, right, top and botton. The colourbar will be of the elevation.
                        If you want only a hillshade set to none and the cmap to "gray"
        size_format (str): Either geomorphology or big. Anything else gets you a 4.9 inch wide figure (standard ESURF size)
        fig_format (str): An image format. png, pdf, eps, svg all valid
        dpi (int): The dots per inch of the figure
        out_fname_prefix (str): The prefix of the image file. If blank uses the fname_prefix


    Returns:
        A string with the name of the image (printed to file): Shaded relief plot with the basins coloured by basin ID. Uses a colourbar to show each basin

    Author: FJC, SMM
    """

    # set figure sizes based on format
    if size_format == "geomorphology":
        fig_width_inches = 6.25
    elif size_format == "big":
        fig_width_inches = 16
    else:
        fig_width_inches = 4.92126

    # get the basin IDs to make a discrete colourmap for each ID
    BasinInfoDF = PlotHelp.ReadBasinInfoCSV(DataDirectory, fname_prefix)

    basin_keys = list(BasinInfoDF['basin_key'])
    basin_keys = [int(x) for x in basin_keys]

    basin_junctions = list(BasinInfoDF['outlet_junction'])
    basin_junctions = [float(x) for x in basin_junctions]

    print ('Basin keys are: ')
    print (basin_keys)

    # going to make the basin plots - need to have bil extensions.
    print("I'm going to make the basin plots. Your topographic data must be in ENVI bil format or I'll break!!")



    # clear the plot
    plt.clf()

    # get the rasters
    raster_ext = '.bil'
    #BackgroundRasterName = fname_prefix+raster_ext
    HillshadeName = fname_prefix+'_hs'+raster_ext
    BasinsName = fname_prefix+'_AllBasins'+raster_ext
    print (BasinsName)
    Basins = LSDV.GetBasinOutlines(DataDirectory, BasinsName)

    # If wanted, add the labels
    if add_basin_labels:
        print("I am going to add basin labels, there will be no colourbar.")
        MF = MapFigure(HillshadeName, DataDirectory,coord_type="UTM_km", colourbar_location="None")
        MF.plot_polygon_outlines(Basins, linewidth=0.8)
        MF.add_drape_image(BasinsName, DataDirectory, colourmap = cmap, alpha = 0.8, colorbarlabel='Basin ID', discrete_cmap=True, n_colours=len(basin_keys), show_colourbar = False, modify_raster_values=True, old_values=basin_junctions, new_values=basin_keys, cbar_type = int)

        # This is used to label the basins
        label_dict = dict(zip(basin_junctions,basin_keys))
        # this dict has the basin junction as the key and the basin_key as the value

        Points = LSDV.GetPointWithinBasins(DataDirectory, BasinsName)
        MF.add_text_annotation_from_shapely_points(Points, text_colour='k', label_dict=label_dict)
    else:
        print("I am showing the basins without text labels.")
        MF = MapFigure(HillshadeName, DataDirectory,coord_type="UTM_km", colourbar_location=cbar_loc)
        MF.plot_polygon_outlines(Basins, linewidth=0.8)
        MF.add_drape_image(BasinsName, DataDirectory, colourmap = cmap, alpha = 0.8, colorbarlabel='Basin ID', discrete_cmap=True, n_colours=len(basin_keys), show_colourbar = True, modify_raster_values=True, old_values=basin_junctions, new_values=basin_keys, cbar_type = int)

    # Save the image
    thing_to_return = []
    if (save_fig):
        if len(out_fname_prefix) == 0:
            ImageName = DataDirectory+fname_prefix+"_basins."+fig_format
        else:
            ImageName = DataDirectory+out_fname_prefix+"_basins."+fig_format

        MF.save_fig(fig_width_inches = fig_width_inches, FigFileName = ImageName, FigFormat=fig_format, Fig_dpi = dpi, transparent=True)

        thing_to_return = ImageName

    else:
        fig = MF.save_fig(fig_width_inches = fig_width_inches, transparent=True, return_fig = True)
        thing_to_return = fig

    print("I'm returning:")
    print(thing_to_return)
    return thing_to_return



def PrintBasins_Complex(DataDirectory,fname_prefix,
                   use_keys_not_junctions = True, show_colourbar = False,
                   Remove_Basins = [], Rename_Basins = {}, Value_dict= {},
                   cmap = "jet", colorbarlabel = "colourbar", size_format = "ESURF",
                   fig_format = "png", dpi = 250, out_fname_prefix = "", include_channels = False, label_basins = True, save_fig = True):
    """
    This function makes a shaded relief plot of the DEM with the basins coloured
    by the basin ID.

    Args:
        DataDirectory (str): the data directory with the m/n csv files
        fname_prefix (str): The prefix for the m/n csv files
        use_keys_not_junctions (bool): If true use basin keys to locate basins, otherwise use junction indices
        show_colourbar (bool): if true show the colourbar
        Remove_Basins (list): A lists containing either key or junction indices of basins you want to remove from plotting
        Rename_Basins (dict): A dict where the key is either basin key or junction index, and the value is a new name for the basin denoted by the key
        Value_dict (dict): A dict where the key is either basin key or junction index, and the value is a value of the basin that is used to colour the basins
        add_basin_labels (bool): If true, label the basins with text. Otherwise use a colourbar.
        cmap (str or colourmap): The colourmap to use for the plot
        cbar_loc (str): where you want the colourbar. Options are none, left, right, top and botton. The colourbar will be of the elevation.
                        If you want only a hillshade set to none and the cmap to "gray"
        size_format (str): Either geomorphology or big. Anything else gets you a 4.9 inch wide figure (standard ESURF size)
        fig_format (str): An image format. png, pdf, eps, svg all valid
        dpi (int): The dots per inch of the figure
        out_fname_prefix (str): The prefix of the image file. If blank uses the fname_prefix
        include_channels (bool): If true, adds a channel plot. It uses the chi_data_maps file
        label_basins (bool): If true, the basins get labels

    Returns:
        A string with the name of the image (printed to file): Shaded relief plot with the basins coloured by basin ID. Uses a colourbar to show each basin. This allows more complex plotting with renamed and excluded basins.

    Author: FJC, SMM
    """

    # set figure sizes based on format
    if size_format == "geomorphology":
        fig_width_inches = 6.25
    elif size_format == "big":
        fig_width_inches = 16
    else:
        fig_width_inches = 4.92126

    # get the basin IDs to make a discrete colourmap for each ID
    BasinInfoDF = PlotHelp.ReadBasinInfoCSV(DataDirectory, fname_prefix)

    basin_keys = list(BasinInfoDF['basin_key'])
    basin_keys = [int(x) for x in basin_keys]

    basin_junctions = list(BasinInfoDF['outlet_junction'])
    basin_junctions = [float(x) for x in basin_junctions]

    print ('Basin keys are: ')
    print (basin_keys)

    # going to make the basin plots - need to have bil extensions.
    print("I'm going to make the basin plots. Your topographic data must be in ENVI bil format or I'll break!!")

    # clear the plot
    plt.clf()

    # get the rasters
    raster_ext = '.bil'
    #BackgroundRasterName = fname_prefix+raster_ext
    HillshadeName = fname_prefix+'_hs'+raster_ext
    BasinsName = fname_prefix+'_AllBasins'+raster_ext

    # This initiates the figure
    MF = MapFigure(HillshadeName, DataDirectory,coord_type="UTM_km", colourbar_location="None")

    # This adds the basins
    MF.add_basin_plot(BasinsName,fname_prefix,DataDirectory, mask_list = Remove_Basins,
                      rename_dict = Rename_Basins, value_dict = Value_dict,
                      use_keys_not_junctions = use_keys_not_junctions, show_colourbar = show_colourbar,
                      discrete_cmap=True, n_colours=15, colorbarlabel = colorbarlabel,
                      colourmap = cmap, adjust_text = False, label_basins = label_basins)

    # See if you need the channels
    if include_channels:
        print("I am going to add some channels for you")
        ChannelFileName = fname_prefix+"_chi_data_map.csv"
        chi_csv_fname = DataDirectory+ChannelFileName

        thisPointData = LSDP.LSDMap_PointData(chi_csv_fname)

        MF.add_point_data(thisPointData,column_for_plotting = "basin_key",
                       scale_points = True,column_for_scaling = "drainage_area",
                       this_colourmap = "Blues_r", scaled_data_in_log = True,
                       max_point_size = 3, min_point_size = 1, discrete_colours = True, NColours = 1, zorder = 5)

    # Save the image
    thing_to_return = []
    if (save_fig):
        if len(out_fname_prefix) == 0:
            ImageName = DataDirectory+fname_prefix+"_selected_basins."+fig_format
        else:
            ImageName = DataDirectory+out_fname_prefix+"_selected_basins."+fig_format

        MF.save_fig(fig_width_inches = fig_width_inches, FigFileName = ImageName, FigFormat=fig_format, Fig_dpi = dpi, transparent=True)

        thing_to_return = ImageName

    else:
        fig = MF.save_fig(fig_width_inches = fig_width_inches, transparent=True, return_fig = True)
        thing_to_return = fig

    print("I'm returning:")
    print(thing_to_return)
    return thing_to_return


def SimpleProfile(DataDirectory,fname_prefix, size_format = "ESURF", fig_format = "png", dpi = 250, basin_key=[0], source_key=[0], use_chi = False):
    """
    This function makes a simple river long profile plot from the chi data map.

    Args:
        DataDirectory (str): the data directory
        fname_prefix (str): the name of the DEM without extension
        FigFormat(str): format of the figure, e.g. png, svg
        size_format (str): size of the figure, can be either 'geomorphology', 'big', or 'ESURF'
        basin_key (list): basin keys to analyse
        source_key (list): source keys of the channels you want to plot.

    Returns:
        long profile plot

    Author: FJC
    """

    fname = LSDCP.ChannelProfilePlot(DataDirectory, fname_prefix, FigFormat=fig_format, size_format=size_format, dpi = dpi, basin_key=basin_key, source_key=source_key,use_chi = use_chi)

    return fname



def PrintCategorised(DataDirectory,fname_prefix, Drape_prefix,
                     show_colourbar = False,
                     cmap = "jet", cbar_loc = "right", cbar_label = "drape colourbar", size_format = "ESURF",
                     fig_format = "png", dpi = 250, out_fname_prefix = ""):
    """
    This function makes a shaded relief plot of the DEM a drape plot that has categorised colours.

    Args:
        DataDirectory (str): the data directory with the m/n csv files
        fname_prefix (str): The prefix for the m/n csv files
        Drape_prefix (str): The prefix of the drape name
        show_colourbar (bool): if true show the colourbar
        cmap (str or colourmap): The colourmap to use for the plot
        cbar_loc (str): where you want the colourbar. Options are none, left, right, top and botton. The colourbar will be of the elevation.
                        If you want only a hillshade set to none and the cmap to "gray"
        cbar_label (str): The text on the colourbar label
        size_format (str): Either geomorphology or big. Anything else gets you a 4.9 inch wide figure (standard ESURF size)
        fig_format (str): An image format. png, pdf, eps, svg all valid
        dpi (int): The dots per inch of the figure
        out_fname_prefix (str): The prefix of the image file. If blank uses the fname_prefix

    Returns:
        A string with the name of the image (printed to file): Shaded relief plot with categorised data.

    Author: SMM
    """

    # set figure sizes based on format
    if size_format == "geomorphology":
        fig_width_inches = 6.25
    elif size_format == "big":
        fig_width_inches = 16
    else:
        fig_width_inches = 4.92126



    # going to make the basin plots - need to have bil extensions.
    print("I'm going to make a plot of categorised data. Your topographic data must be in ENVI bil format or I'll break!!")

    # get the rasters
    raster_ext = '.bil'
    #BackgroundRasterName = fname_prefix+raster_ext
    BackgroundRasterName = fname_prefix+'_hs'+raster_ext
    CatName = Drape_prefix+raster_ext

    # clear the plot
    plt.clf()

    # set up the base image and the map
    MF = MapFigure(BackgroundRasterName, DataDirectory,coord_type="UTM_km",colourbar_location = cbar_loc)
    #MF.add_drape_image(ElevationName,DataDirectory,colourmap = "gray", alpha = 0.6, colorbarlabel = None)
    MF.add_categorised_drape_image(CatName,DataDirectory,colourmap = cmap, alpha = 0.7, colorbarlabel = cbar_label, norm = "none")


    # Save the image
    if len(out_fname_prefix) == 0:
        ImageName = DataDirectory+fname_prefix+"_categorised."+fig_format
    else:
        ImageName = DataDirectory+out_fname_prefix+"_categorised."+fig_format

    MF.save_fig(fig_width_inches = fig_width_inches, FigFileName = ImageName, FigFormat=fig_format, Fig_dpi = dpi, transparent=True) # Save the figure


