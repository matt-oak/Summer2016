# OpenTopoDL
###### A python script to download data in bulk from [OpenTopo](http://opentopo.sdsc.edu)

## Description

[OpenTopo](http://opentopo.sdsc.edu) is home to a mass of free, accessible topography data. This data is available in 2 different formats,
Lidar Point Cloud and Raster. The purpose of this python script is to automate the manual process of selecting a dataset and downloading
the available data. 


### Running w/ User Input
If you don't know what format of data you want and/or the numbers corresponding to specific datasets on OpenTopo's website, this script
will list the available datasets for download for the data format you request at the expense of your user input. Simply place this
python script in the directory you wish to download data to and run:

```>python OpenTopoDL.py```

Once the script has began executing, you will be prompted if you want to download Lidar or Raster data. Input 'l' or 'L' for Lidar data
and 'r' or 'R' for Raster data. Next, the available datasets for that format will be listed. Proceed by inputting the number
corresponding to the dataset you wish to download. Once completed, the data for the specified dataset will be downloaded to your
local machine.

### Running Directly from the Command Line

However, if you already know the data format and the number of the dataset you wish to download, you can run this script directly
from the command line and avoid any user input. Command line arguments are as follows:

1. OpenTopoDL.py
2. 'l' for Lidar data *or* 'r' for Raster data
3. The number of the dataset you wish to download

An example is provided below:

```>python OpenTopoDL.py l 2```

Running this will download the Lidar dataset listed as #2 (Tushar Mountains, Utah) on the OpenTopo website.



