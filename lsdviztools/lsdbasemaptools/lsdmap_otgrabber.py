## lsdmap_otgrabber.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
## These functions are tools to grab DEMs from opentopography (thus ot)
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
## SMM
## 10/07/2020
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#from __future__ import absolute_import, division, print_function, unicode_literals
from __future__ import absolute_import, division, print_function

import pyproj
import numpy as np
import os
import subprocess as sub
import urllib.request
import gdal
from osgeo import ogr, osr
import utm
import shutil
import rasterio as rio
from rasterio.warp import calculate_default_transform, reproject, Resampling



class ot_scraper(object):
    """
    This is the DEM scraper object. You give it some attributes that it then used to download and process DEM data.

    Args:
        source (str): The data source
        longitude_W (float): the western longitude
        longitude_E (float): the eastern longitude
        latitude_S (float): the southern latitude
        latitude_N (float): the northern latitude
        padding (float): how much padding you want around your target area (in decimal degrees)
        path (str): the directory where you want to put your data
        prefix (str): the prefix of thefile to be downloaded

    Returns:
        Creates a DEM_scraper object

    Author: BG and SMM

    Date: 06/07/2020
    """
    def __init__(self, source = "SRTM30", longitude_W = -5.178834, longitude_E = -4.808695, latitude_S = 56.554025, latitude_N = 56.699391, padding = 0, path = "./", prefix = "mySRTM"):
        super(ot_scraper, self).__init__()

        # Registering the attributes
        self.source = source
        self.longitude_W = longitude_W - padding
        self.longitude_E = longitude_E + padding
        self.latitude_S = latitude_S - padding
        self.latitude_N = latitude_N + padding
        self.path = path
        self.prefix = prefix

        if(self.path != "./"):
            os.mkdir(self.path)

    def print_parameters(self):
        """
        This prints the parameters of the scraper object so you don't mess up the download.

        Returns:
            A printing to screen of the parameters

        Author: SMM

        Date: 06/07/2020
        """

        print("The source is: "+self.source)
        print("The west longitude is: "+str(self.longitude_W))
        print("The east longitude is: "+str(self.longitude_E))
        print("The south latitude is: "+str(self.latitude_N))
        print("The north latitude is: "+str(self.latitude_S))
        print("The path is: "+self.path)
        print("The prefix is: "+self.prefix)

    def download_pythonic(self):
        """
        This downloads the DEM. Call it once the DEM_scraper object is created. Uses a pythonic version that doesn't have system calls

        Returns:
            The filename, the path, and the filename without the path. And in addition downloads the DEM

        Author: SMM

        Date: 06/07/2020
        """
        if(self.source == "SRTM30"):
            str_source = "SRTMGL1"
        if(self.source == "SRTM90"):
            str_source = "SRTMGL3"
        if(self.source == "alos"):
            str_source = "AW3D30"

        url_string = 'https://portal.opentopography.org/otr/getdem?demtype=%s&south=%s&north=%s&west=%s&east=%s&outputFormat=GTiff'%(str_source,self.latitude_S,self.latitude_N,self.longitude_W,self.longitude_E, )
        filename = self.path+self.prefix+"_"+self.source + ".tif"
        fwithoutpath= self.prefix+"_"+self.source + ".tif"


        print("I am going to download the following for you:")
        print(url_string)
        print("This might take a little while, depending on the size of the file. ")

        # Download the file from `url` and save it locally under `file_name`:
        with urllib.request.urlopen(url_string) as response, open(filename, 'wb') as out_file:
            shutil.copyfileobj(response, out_file)

        print("Finished downloading")
        return filename,self.path,fwithoutpath


    def download(self):
        """
        This downloads the DEM. Call it once the DEM_scraper object is created.

        Returns:
            Filename, path, and fielname without path, but downloads a DEM

        Author: BG

        Date: 06/07/2020
        """
        if(self.source == "SRTM30"):
            str_source = "SRTMGL1"
        if(self.source == "SRTM90"):
            str_source = "SRTMGL3"
        if(self.source == "alos"):
            str_source = "AW3D30"


        wget_command = 'curl -X GET "https://portal.opentopography.org/API/globaldem?demtype=%s&south=%s&north=%s&west=%s&east=%s&outputFormat=GTiff" -H "accept: */*" > %s'%(str_source,self.latitude_S,self.latitude_N,self.longitude_W,self.longitude_E, self.path+self.prefix+"_"+self.source + ".tif")
        sub.call(wget_command, shell = True)

        filename = self.path+self.prefix+"_"+self.source + ".tif"
        fnamewithoutpath = self.prefix+"_"+self.source + ".tif"

        return filename,self.path,fnamewithoutpath


    def to_UTM_pythonic(self):
        """
        Converts the DEM to UTM coordinate system. Automatically checks the UTM zone using the python package utm. Uses GDAL command line to do this

        Returns:
            bil (bool): If true, convert to ENVI bil format

        Author: SMM

        Date: 06/07/2020
        """

        filename = self.path+self.prefix+"_"+self.source + ".tif"

        # First get the source coordinate system
        # open dataset
        ds = gdal.Open(filename)
        prj=ds.GetProjection()
        print("The projections is:")
        print(prj)
        ds = []

        print("And some extra projection information strings:")
        srs=osr.SpatialReference(wkt=prj)
        if srs.IsProjected:
            print(srs.GetAttrValue('projcs'))
        print(srs.GetAttrValue('geogcs'))

        # now do it with rasterio
        dem_data = rio.open(filename)
        print(dem_data.meta)


        temp_info = utm.from_latlon((self.latitude_S+self.latitude_N)/2, (self.longitude_W + self.longitude_E)/2)
        if(temp_info[3] in ['X','W','V','U','T','S','R','Q','P','N']):
            south = False
        else:
            south = True

        res = 30.0
        if(self.source == "SRTM90"):
            res=90.0

        UTMzone = temp_info[2]
        if south:
            EPSG = "327" + str(UTMzone)
        else:
            EPSG = "326" + str(UTMzone)

        res_tuple = (res,res)
        print("res tuple is:")
        print(res_tuple)

        dst_crs = 'EPSG:'+EPSG
        print("The destination CRS is: "+dst_crs)
        output_filename = self.path+self.prefix+"_"+self.source + "_UTM.tif"


        with rio.open(filename) as src:
            transform, width, height = calculate_default_transform(
                src.crs, dst_crs, src.width, src.height, resolution=res_tuple,*src.bounds)
            kwargs = src.meta.copy()
            kwargs.update({
                'crs': dst_crs,
                'transform': transform,
                'width': width,
                'height': height
            })

            with rio.open(output_filename, 'w', **kwargs) as dst:
                for i in range(1, src.count + 1):
                    reproject(
                        source=rio.band(src, i),
                        destination=rio.band(dst, i),
                        src_transform=src.transform,
                        src_crs=src.crs,
                        dst_resolution=res_tuple,
                        dst_transform=transform,
                        dst_crs=dst_crs,
                        resampling=Resampling.cubic)
        dem_datam2 = rio.open(output_filename)

        print(dem_datam2.meta)



    def to_UTM(self, bil = False):
        """
        Converts the DEM to UTM coordinate system. Automatically checks the UTM zone using the python package utm. Uses GDAL command line to do this

        Returns:
            bil (bool): If true, convert to ENVI bil format

        Author: BG

        Date: 06/07/2020
        """
        temp_info = utm.from_latlon((self.latitude_S+self.latitude_N)/2, (self.longitude_W + self.longitude_E)/2)
        if(temp_info[3] in ['X','W','V','U','T','S','R','Q','P','N']):
            south = False
        else:
            south = True

        res = 30
        if(self.source == "SRTM90"):
            res=90

        UTMzone = temp_info[2]
        if south:
            EPSG = "+proj=utm +zone="+str(UTMzone)+" +south +datum=WGS84"
        else:
            EPSG = "+proj=utm +zone="+str(UTMzone)+" +datum=WGS84"

        if(bil):
            output_format = "-of ENVI"
            ext = ".bil"
        else:
            output_format = ""
            ext = ".tif"


        gdal_command = "gdalwarp -t_srs '%s' -tr %s %s -r cubic %s %s %s "%(EPSG, res, res, output_format, self.path+self.prefix+"_"+self.source+ ".tif", self.path+self.prefix+"_"+self.source + "_UTM" + ext)
        print("Calling gdal with:")
        print(gdal_command)
        sub.call(gdal_command, shell = True)


