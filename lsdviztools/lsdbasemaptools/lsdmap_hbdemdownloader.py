## lsdmap_hbdemdownloader.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
## These functions allow you to download DEMs based on HydroBasins (Lehner &
## Grill, 2013). This code is one level higher than the
## ot_scraper and therefore downloads DEMs from OpenTopography.
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
## RV
## 31/01/2025
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=

## IMPORTANT this script uses lsdmap_otgrabber and lsdmap_gdalio
## Thus, these scripts should never import this hbdemdownloader or otherwise
## it will result in circular imports.
from .lsdmap_otgrabber import ot_scraper
from ..lsdplottingtools import lsdmap_gdalio as gio

import geopandas as gpd
import pandas as pd
import numpy as np
import utm
import os
import rasterio
from shapely.geometry import mapping
from rasterio.mask import mask
from pyproj import CRS

class hb_demdownloader(object):
    """
    The HydroBASINS DEM downloader object. You initialise the object with
    one or more hydrobasins, and then there are functions for things like
    buffering the hydrobasins, downloading the DEM using ot_scraper, etc.

    Args:
        hydrobasins_ids (list of ints): a list of one or multiple hydrobasin ids that
            you want to work with. Does not need to be in the same pfaf level.
        filepath_to_hydrobasins (str): the path to your hydrobaisins directory.
            The directory must contain shapefiles that start with "hybas_na_lev".

    Author: RV
    Date: 31/01/2025
    """
    def __init__(self, hydrobasins_ids = [], filepath_to_hydrobasins = "./hydrobasins"):
        list_geoms = []
        for hydrobasin_id in hydrobasins_ids:
            # get filepath right
            pfaf_lvl = str(hydrobasin_id)[1:3]
            hydrobasin_filepath = filepath_to_hydrobasins + '/hybas_na_lev'+pfaf_lvl+'_v1c.shp'
            print(f"I am going to find the Hydrobasin with id {str(hydrobasin_id)} in the file: {hydrobasin_filepath}")

            # open file, get selected basin 
            hydrobasin_shp = gpd.read_file(hydrobasin_filepath)
            selected_hydrodrobasin = hydrobasin_shp.loc[hydrobasin_shp["HYBAS_ID"]==hydrobasin_id]

            # reproject geometry of hydrobasin to corresponding UTM zone
            hydrobasin_geometry = selected_hydrodrobasin.geometry.iloc[0]
            lat, lon = hydrobasin_geometry.centroid.y, hydrobasin_geometry.centroid.x
            zone_number = utm.from_latlon(lat, lon)[2]
            hemisphere = "north" if lat >= 0 else "south"
            epsg_code = f'327{zone_number}' if hemisphere == 'south' else f'326{zone_number}'
            crs = CRS.from_epsg(epsg_code)
            selected_hydrodrobasin = selected_hydrodrobasin.to_crs(crs)

            # add selected hydrobasin to the geometries_gdf
            list_geoms.append(selected_hydrodrobasin)
        self.geometries_gdf = gpd.GeoDataFrame(pd.concat(list_geoms, ignore_index = True))
        print("I have now loaded in the shapes of your Hydrobasins.")

    def buffer_hydrobasins(self):
        """
        Function to buffer each hydrobasin according to a radius determined
        by its area, following Strong and Mudd (2022)

        Author: RV
        Date: 31/01/2025
        """
        print("Starting buffering")
        buffered_geometries = []
        for idx, row in self.geometries_gdf.iterrows():
            # find buffer radius
            basin_area = row.iloc[6]
            if basin_area < 100:
                buffer_radius = 2*1000
            elif basin_area > 15625:
                buffer_radius = 25*1000
            else:
                buffer_radius = 0.25*np.sqrt(basin_area)*1000
            
            # buffer geometry
            buffered_hydrobasin_geometry = row.geometry.buffer(buffer_radius)
            buffered_geometries.append(buffered_hydrobasin_geometry)

        # Update the geometries in the dataframe
        self.geometries_gdf['geometry'] = gpd.GeoSeries(buffered_geometries)
        print("Finished buffering")
    
    def merge_all_geometries_by_unary_union(self):
        """
        Function to merge the polygon geometries (hydrobasins) in the dataframe by unary union,
        to become one big polygon.

        Author: RV
        Date: 31/01/2025
        """
        print(f"Taking unary onion of all my {len(self.geometries_gdf)} geometries.")
        unioned_geometry = self.geometries_gdf.unary_union
        self.geometries_gdf = gpd.GeoDataFrame([{'geometry':unioned_geometry}], crs = self.geometries_gdf.crs)
        print(f"I now consist of {len(self.geometries_gdf)} geometry.")

    def make_geometries_intersect_with_supplied_geoseries(self, input_geoseries):
        """
        Function to find the intersection of geometries with a supplied geoseries.
        You can only suppply one geoseries to intersect all your geometries with. 
        Intersection(s) are saved as new geometries.

        Args:
            input_geoseries (GeoSeries): The geoseries to intersect with, has to
                have the right crs for that data.

        Author: RV
        Date: 31/01/2025
        """
        print(f"Taking intersection of each of my {len(self.geometries_gdf)} geometries with your input geoseries")
        # set input geoseries crs to that of the geometries gdf
        input_geoseries = input_geoseries.to_crs(self.geometries_gdf.crs)

        # get unary union of input geoseries
        input_geometry = input_geoseries.unary_union

        # get geometries of intersections as list
        intersections = [row.geometry.intersection(input_geometry) for index, row in self.geometries_gdf.iterrows()]

        # change geometries column of geometries gdf to that of the intersections
        self.geometries_gdf['geometry'] = intersections

        # remove geometries that are not present in intersection
        self.geometries_gdf = self.geometries_gdf[~self.geometries_gdf['geometry'].is_empty]
        print(f"Finished. I removed any 'empty' intersections and now consist of {len(self.geometries_gdf)} geometries.")  

    def setup_directories_and_download_DEMs(self, directory_path = "./Data", Dataset_prefixes = [], source_name = "COP30", OT_api_key_file = "my_OT_api_key.txt"):
        """
        This function takes an existing data directory, then downloads DEMs from OpenTopography 
        for each geometry in the geometries geodataframe. Downloaded into a subdirectory named 
        according to the supplied dataset prefix. Converts tifs to LSDTT-readable ENVI bils.
        
        Args:
            directory_path (str): the path name of the data directory that is to 
                be created. Will throw error if it already exists.
            Dataset_prefixes (list of str): the dataset prefix that is to be used
                for each geometry. List needs to have the length of the number of
                geometries.
            source_name (str): the source name of the DEM dataset, default COP30
            OT_api_key_file (str): a text file with your OpenTopography API Key
        """
        print("Going to setup directories and dowload DEMs for your geometries.")
        # check if there are as many dataset_prefixes as rows in gdf
        if (len(self.geometries_gdf) != len(Dataset_prefixes)):
            print(f"Your number of dataset prefixes ({len(Dataset_prefixes)}) does not match the number of geometries ({len(self.geometries_gdf)}).")
            return
        # make sure API key file is correct
        with open(OT_api_key_file, 'r') as file:
            print("I am reading you OT API key from the file "+OT_api_key_file)
            api_key = file.read().rstrip()
            print("Your api key starts with: "+api_key[0:4])

        # make copy of geometries_gdf in epsg 4326 to find coordinates for ot
        geometries_gdf_epsg4326 = self.geometries_gdf.copy()
        geometries_gdf_epsg4326 = geometries_gdf_epsg4326.to_crs(epsg=4326)

        # loop through geometries
        for idx, row in self.geometries_gdf.iterrows():
            # get dataset prefix and directory for this geometry
            Dataset_prefix = Dataset_prefixes[idx]
            DataDirectory = f"{directory_path}/{Dataset_prefix}/"
            print(f"Now working on {Dataset_prefix}.")

            # check if data directory already exists, if not, will give error
            if os.path.exists(DataDirectory) == True:
                print(f"The directory {DataDirectory} already exists. I am not going to download data into this folder.")
                continue
            
            # get upper right and lower left coordinates of geometry
            envelope = geometries_gdf_epsg4326.iloc[idx]['geometry'].envelope
            bounds = envelope.bounds
            ll = [bounds[1], bounds[0]] 
            ur = [bounds[3], bounds[2]]

            # download DEM and convert for LSDTT
            DEM = ot_scraper(source = source_name,
                         lower_left_coordinates = ll,
                         upper_right_coordinates = ur,
                         prefix = Dataset_prefix+"_not_clipped",
                         api_key_file = OT_api_key_file,
                         path = DataDirectory)
            DEM.print_parameters()
            DEM.download_pythonic()
            gio.convert4lsdtt(DataDirectory,Dataset_prefix+"_not_clipped_"+source_name+".tif") 

            # clip raster to geometry
            raster_in = DataDirectory+Dataset_prefix+"_not_clipped_"+source_name+"_UTM.bil"
            raster_out = DataDirectory+Dataset_prefix+"_"+source_name+"_UTM.bil"
            geometry = self.geometries_gdf.iloc[idx]['geometry']
            geometry_geojson = mapping(geometry)
            coords = [geometry_geojson]
            #coords = [json.loads(geoseries.to_json())['features'][0]['geometry']]
            with rasterio.open(raster_in) as src:
                out_image, out_transform = mask(src, shapes=coords, crop=True)
                out_meta = src.meta

            out_meta.update({"driver":"ENVI",
                     "height":out_image.shape[1],
                     "width":out_image.shape[2],
                     "transform":out_transform})

            with rasterio.open(raster_out, "w", **out_meta) as dest:
                dest.write(out_image)
            
            # remove unwanted files
            os.remove(DataDirectory+Dataset_prefix+"_not_clipped_"+source_name+"_UTM.bil")
            os.remove(DataDirectory+Dataset_prefix+"_not_clipped_"+source_name+"_UTM.bil.aux.xml")
            os.remove(DataDirectory+Dataset_prefix+"_not_clipped_"+source_name+"_UTM.hdr")
            os.remove(DataDirectory+Dataset_prefix+"_not_clipped_"+source_name+"_UTM.tif")
            os.remove(DataDirectory+Dataset_prefix+"_not_clipped_"+source_name+".tif")

        print("Finished downloading DEMs for your geometries")
            