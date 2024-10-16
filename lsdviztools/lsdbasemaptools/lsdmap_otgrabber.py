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
from osgeo import gdal
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
        prefix (str): the prefix of the file to be downloaded
        resolution (float): the desired grid resolution (gdal will resample)
        api_key_file (str): A filename that holds your api key
        lower_left_coordinates (float list): a two element list of the latitude and longitude of the lower left corner. Overwrites the other edge coordinates
        upper_right_coordinates (float list): a two element list of the latitude and longitude of the upper right corner. Overwrites the other edge coordinates

    Returns:
        Creates a DEM_scraper object

    Author: BG and SMM

    Date: 06/07/2020
    """
    def __init__(self, source = "SRTMGL1", longitude_W = -5.178834 , longitude_E = -4.808695, 
                       latitude_S = 56.554025, latitude_N = 56.699391, 
                       padding = 0, path = "./", prefix = "mySRTM",
                       resolution = 30, api_key_file = "NULL", 
                       lower_left_coordinates = [], upper_right_coordinates = []):
        super(ot_scraper, self).__init__()

        
        # The kind of download
        self.download_type = "global"
        
        # Registering the attributes
        self.source = source

        if (len(lower_left_coordinates) == 2):
            print("I am taking your coordinates from the lower left list")
            self.longitude_W = lower_left_coordinates[1]
            self.latitude_S = lower_left_coordinates[0]
        else:
            self.longitude_W = longitude_W
            self.latitude_S = latitude_S            
        if (len(upper_right_coordinates) == 2):
            print("I am taking your coordinates from the upper right list")
            self.longitude_E = upper_right_coordinates[1]
            self.latitude_N = upper_right_coordinates[0]
        else:
            self.longitude_E = longitude_E
            self.latitude_N = latitude_N            


        self.longitude_W = self.longitude_W - padding
        self.longitude_E = self.longitude_E + padding
        self.latitude_S = self.latitude_S - padding
        self.latitude_N = self.latitude_N + padding
        self.path = path
        self.prefix = prefix
        self.resolution = resolution
        self.api_key_file = api_key_file

  
        
        if( self.longitude_W > self.longitude_E ):
            print("Your west edge is to the east of you east edge.")
            print("Go back and check your coordinates")
            exit()
        if( self.latitude_S > self.latitude_N ):
            print("Your north edge is to the south of you south edge.")
            print("Go back and check your coordinates")
            exit()

        if(self.source == "SRTM30"):
            self.source = "SRTMGL1"
        if(self.source == "SRTM90"):
            self.source = "SRTMGL3"
        if(self.source == "alos"):
            self.source = "AW3D30"
        if(self.source == "otCatalog"):
            self.source = "otcatalog"
            
        USGS_list = ["USGS30m", "USGS10m", "USGS1m"]
        if (self.source == "USGS1m"):
            print("You are asking for a USGS 1m raster: if you do not have an academic account at opentopography this won't work")
            
        
        if (self.source in USGS_list):
            self.download_type = "usgsdem"

        
        ninety_list = ["SRTMGL3","COP90"]
        fivehunnert_list = ["SRTM15Plus","GEBCOIceTopo","GEBCOSubIceTopo"]

        if(self.api_key_file=="NULL"):
            print("Opentopography requires an API key.")
            print("You need to create an opentopography account and get one")
            print("When you have your key, put it in a file and set the filename")
            print("NEVER upload this file to a repository. It is your private key")
            exit()
        
        with open(self.api_key_file, 'r') as file:
            print("I am reading you OT API key from the file "+self.api_key_file)
            self.api_key = file.read().rstrip()

            
        
        if (self.source in ninety_list):
            print("Your source is a 90m DEM.")
            self.resolution = 90
        elif (self.source == "USGS10m"):
            print("You have chosen a USGS 10m DEM")
            self.resolution = 10
        elif (self.source == "USGS1m"):
            self.resolution = 1   
            print("You have chosen a USGS 1m DEM. This requires you to have approval from opentopography.")
        elif (self.source in fivehunnert_list):
            print("Your source has 500 m grid spacing")
            self.resolution = 500
        elif (self.source == "GEDI_L3"):
            print("Your source has 1000 m grid spacing")
            self.resolution = 1000
        else:
            self.resolution = 30
            
        print("The grid spacing for your DEM will be:" + str(self.resolution))


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
        print("The grid spacing is: "+str(self.resolution))

    def download_pythonic(self):
        """
        This downloads the DEM. Call it once the DEM_scraper object is created. Uses a pythonic version that doesn't have system calls

        Returns:
            The filename, the path, and the filename without the path. And in addition downloads the DEM

        Author: SMM

        Date: 06/07/2020
        """

    
        if(self.api_key=="NULL"):
            print("I cannot download data without an API key")
            exit()
            
        url_string = "NULL"
        url_string_no_api = "NULL"
        if(self.download_type == "global"):
            url_string = 'https://portal.opentopography.org/API/globaldem?demtype=%s&south=%s&north=%s&west=%s&east=%s&outputFormat=GTiff&API_Key=%s'%(self.source,self.latitude_S,self.latitude_N,self.longitude_W,self.longitude_E,self.api_key )

            url_string_no_api = 'https://portal.opentopography.org/API/globaldem?demtype=%s&south=%s&north=%s&west=%s&east=%s&outputFormat=GTiff'%(self.source,self.latitude_S,self.latitude_N,self.longitude_W,self.longitude_E)             
        elif(self.download_type == "usgsdem"):
            url_string = 'https://portal.opentopography.org/API/usgsdem?datasetName=%s&south=%s&north=%s&west=%s&east=%s&outputFormat=GTiff&API_Key=%s'%(self.source,self.latitude_S,self.latitude_N,self.longitude_W,self.longitude_E,self.api_key )

            url_string_no_api = 'https://portal.opentopography.org/API/usgsdem?datasetName=%s&south=%s&north=%s&west=%s&east=%s&outputFormat=GTiff'%(self.source,self.latitude_S,self.latitude_N,self.longitude_W,self.longitude_E)  
           
            
        filename = self.path+self.prefix+"_"+self.source + ".tif"
        fwithoutpath= self.prefix+"_"+self.source + ".tif"


       
        
        
        print("I am going to download a file from opentopography (I've removed the API key):")
        print(url_string_no_api)
        print("This might take a little while, depending on the size of the file. ")

        print("The filename will be:")
        print(filename)

        print("The path and file without path are:")
        print(self.path + "  "+ fwithoutpath)

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
        self.download_pythonic()


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
        print("The projection is:")
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

        print("My grid spacing is: "+str(self.resolution))
        res = self.resolution

        UTMzone = temp_info[2]
        if south:
            EPSG = f"327{UTMzone:02d}"
        else:
            EPSG = f"326{UTMzone:02d}"

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

        res = self.resolution
        print("The resolution is: "+ str(res))

        UTMzone = temp_info[2]
        
           
        if south:
            EPSG = "+proj=utm +zone="+f"327{UTMzone:02d}"+" +south +datum=WGS84"
        else:
            EPSG = "+proj=utm +zone="+f"326{UTMzone:02d}"+" +datum=WGS84"

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


