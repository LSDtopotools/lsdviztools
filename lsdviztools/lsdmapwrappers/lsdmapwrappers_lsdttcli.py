## lsdmapwrappers_lsdttcli.py
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
## This allows python users to call the lsdtt commang line interface
## It only works if lsdtt is installed
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
## SMM
## 10/07/2020
##=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=
#from __future__ import absolute_import, division, print_function, unicode_literals
from __future__ import absolute_import, division, print_function
import os
from os import path
import subprocess

class lsdtt_driver(object):
    """
    This is the lsdtt command line interface object

    Args:
        command_line_tool (str): The data source
        driver_name (str): A name of the driver file that will be written when a call to the command line is made
        read_path (str): the directory from which you read your data
        write_path (str): the directory where want to put your data
        prefix (str): the prefix of DEM to be processed
        parameter_dictionary (dict): A dictionary that stores all the parameter names for the lsdtt call

    Returns:
        Creates a lsdtt_driver object

    Author: SMM

    Date: 10/07/2020
    """
    def __init__(self, command_line_tool = "lsdtt-basic-metrics", driver_name = "Test_01", read_path = "./", write_path = "./", read_prefix = "mySRTM", write_prefix = "mySRTM", parameter_dictionary = {"write_hillshade" : "true", "remove_seas" : "true"}):
        super(lsdtt_driver, self).__init__()

        # Registering the attributes
        self.command_line_tool = command_line_tool
        self.driver_name = driver_name
        self.parameter_dictionary = parameter_dictionary
        self.read_path = read_path
        self.write_path = write_path
        self.read_prefix = read_prefix
        self.write_prefix = write_prefix

        if(self.read_path != "./"):
            if not path.exists(self.read_path):
                print("You are trying to load lsdtopotools data in a path that doesn't exist.")
                print("This run is about to crash. Check your read path.")

        if(self.write_path != "./"):
            if not path.exists(self.write_path):
                os.mkdir(self.write_path)

        self.check_command_line_tools()
        print("The lsdtopotools command line tools available are: ")
        print(["lsdtt-basic-metrics","lsdtt-channel-extraction","lsdtt-chi-mapping","lsdtt-cosmo-tool","lsdtt-hillslope-channel-coupling"])
        print("Please note only lsdtt-basic-metrics has been fully tested")


    def print_parameters(self):
        """
        This prints the parameters of the scraper object so you don't mess up the download.

        Returns:
            A printing to screen of the parameters

        Author: SMM

        Date: 10/07/2020
        """

        print("The command line tool is: "+self.command_line_tool)
        print("The driver name is: "+self.driver_name)
        print("The read path is: "+self.read_path)
        print("The write path is: "+self.write_path)
        print("The read prefix is: "+self.read_prefix)
        print("The write prefix is: "+self.write_prefix)
        print("The parameter dictionary is:")
        print(self.parameter_dictionary)

    def check_command_line_tools(self):
        """
        Makes sure the command line tool is valid

        Returns:
            A bool: true if it is valid, false if it has changed to the default ("lsdtt-basic-metrics")

        Author: SMM

        Date: 10/07/2020
        """

        valid_clt = ["lsdtt-basic-metrics","lsdtt-channel-extraction","lsdtt-chi-mapping","lsdtt-cosmo-tool","lsdtt-hillslope-channel-coupling"]

        if (self.command_line_tool not in valid_clt):
            print("Warning: incorrect command line tool. Defaulting to lsdtt-basic-metrics")
            print("Your options are: ")
            print(valid_clt)
            self.command_line_tool = "lsdtt-basic-metrics"

    def write_lsdtt_driver(self):
        """
        This writes the lsdtt driver file

          Returns:
            A bool: true if it is installed, false if not

        Author: SMM

        Date: 10/07/2020
        """

        with open(self.driver_name+".driver", 'w') as dfile:
            dfile.write("# This is an LSDTopoTools driver file written with the python package lsdviztools\n\n")

            dfile.write("# File locations\n")
            dfile.write("read path: "+self.read_path+"\n")
            dfile.write("write path: "+self.read_path+"\n")
            dfile.write("read fname: "+self.read_prefix+"\n")
            dfile.write("write fname: "+self.write_prefix+"\n")

            dfile.write("\n\n# Now for the parameters\n")

            for parameter, value in self.parameter_dictionary.items():
                dfile.write(parameter+": "+value+"\n")


        print("Done writing the driver file")

    def run_lsdtt_command_line_tool(self):
        """
        Runs the lsdtt command line tool

        Author: SMM

        Date: 10/07/2020
        """

        self.write_lsdtt_driver()

        print("I've finised writing the driver file. Let me run LSDTT for you.")
        subprocess.run([self.command_line_tool,self.driver_name+".driver"])


