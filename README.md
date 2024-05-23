# DEMbuilder
2018-05-18 Brian Wilson <bwilson@co.clatsop.or.us>

## Overview

The goal for this project is to build a high resolution contour layer
for Clatsop County using the best available bare earth lidar.

## Set up

Not sure if I need arcpy but it's currently in the requirements doc.

```bash
conda create -n dembuilder --file=conda_requirements.txt python=3.7.10 -c esri -c conda-forge
conda activate dembuilder
```

## Data

I am using a project called DEMbuilder.aprx to manage all the data
including defining the area to download. Don't forget to log in to ArcGIS
to access the USIEI data referenced in "Downloader map".

Last year I tried to find DEM data but it only covered about 1/2 the
county, so the first step was to find and download the point clouds.

There is a model that will look up the data products available in Clatsop County
and create two (currently) feature classes, lidar_topo and lidar_topobathy
in the project FGDB.

Some of the tile indexes throw a Transformation Warning, but they still get
the job (locating the data I want to download) done so I've been ignoring it.
I think it's because the SRS is incompletely defined; the resultant "tileindex" 
feature classes have no WKID.

### Point cloud data

Coverage information is available as a service from the [USIEI web site](https://coast.noaa.gov/inventory/). I used a model to select polygons that touched the county polygon. Then I created two local feature classes, lidar_topo and lidar_topobathy

This does not really get me anywhere because these feature classes show coverage but not
how to actually download the data. They do also include links to metadata which
might be valuable later.

#### To download tile files

I went to the [NOAA Data Access Viewer](https://coast.noaa.gov/dataviewer/) and drew a rectangle covering Clatsop. I selected interesting data sources and downloaded the tile.zip file for each. I unpacked each tile shapefile and put it in a map.
Maybe using the geopackage files would be better but they don't exist for every dataset.

There is still a hole in the southern part of the county, I will
probably try to fill that with 10m data from NED later on. LATER.

python tile_merge.py

I wrote a script that takes each shapefile and merges them all into the FGDB feature class "tileindex".
Then it takes the county boundary feature class (which I copied into the FGDB for my convenience) and used
"select by location" with a buffer of 2000 meters to select tiles. Finally, it writes "tileindex_clatsop".
Once I had all the tile shapefiles, I selected once again to get only
tiles that are in the county. I merged them all into one shapefile.

Finally, the script puts the name of each source into the tileindex_clatsop file so that the downloader knows where to put them.

#### Download LAZ files

python lidar_downloader.py

The tileindex rows have columns "Name", "source" and "url". Name is the name of
the destination file, and URL is the source where you can download the
file.

This script iterates over the tile index and downloads URL and saves it to source/Name in F:/surface.
If the file has already been downloaded the script will skip it.
If Name has a path in it, it will create the path if it does not exist.

It logs its activities.

It won't overwrite an existing file, so if you need to re-download
something delete the file first then re-run the script. This speeds up
re-running the script to pick up any files it might have failed
to download due to timeouts or other problems.

## Uncompress LAZ files

I think the best way to do this is with the laszip tool.

Download laszip-cli.exe, latest version 3.4.3
from http://lastools.org/download/laszip-cli.exe
and then run

python laz_to_las.py

This script checks each file for errors. I have been thinking it should automatically delete
broken files (input or output), so that you could run the downloader again to get the
missing ones.

## Build DEMs

I probably want to build several at different scales and of course,

* Bare earth
* Highest hit

## Next steps

There is a LiDAR project that has a build_vrt tool

### Contours

There are ContourBuilder and ContourBuilderDocker projects to make contours.

### Other

* slope
* bare earth hillshade
* highest hit hillshade

### Fill in that hole somehow!

Ideas: 

Call up DOGAMI, it looks like a gap in LDC data collection. I tried writing to Jake around 11/2020 but got no answer. Since they have a seamless service they must have gotten data someplace.

I think there is DOGAMI DEM data for that area, that would be another approach - just fill the hole with raster data after converting points to raster.


