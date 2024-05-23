"""
@date:   7/30/2018 12:18:11 PM
@author: bwilson
"""
from __future__ import print_function
import os
import sys
import logging
import arcpy
import glob
from collections import defaultdict

if arcpy.CheckProduct("arcinfo") != "Available": 
    print("Send more money to ESRI.")
    exit(1)

def load(dl,srs):
    workspace = arcpy.env.workspace

    # Make a mosaic for each data provider
    for provider in dl:
        print(provider)

        mosaic_name = provider.replace(' ', '_')
        mosaic_name = mosaic_name.replace('-', '_')
        if mosaic_name[0].isdigit():
            mosaic_name = 'T' + mosaic_name # Ugh...

        mosaic_path = os.path.join(workspace, mosaic_name)
        print("Writing to %s" % mosaic_name)
        if not arcpy.Exists(mosaic_path):
            try:
                arcpy.CreateMosaicDataset_management(in_workspace=workspace, in_mosaicdataset_name=mosaic_name, coordinate_system=srs)
            except Exception as e:
                print(e)
                pass
        for raster_path in dl[provider]:
            raster = os.path.split(raster_path)[1]
            print("\t", raster_path)
#            if os.path.isdir(raster_path):
#                print("still looks ok")
            try:
                # The quotes around raster_path protect us from spaces in the path, apparently.
                arcpy.AddRastersToMosaicDataset_management(mosaic_path, "Raster Dataset", "'%s'" % raster_path,
                   "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "NO_OVERVIEWS", "", 
                   "0", "1500", "", "", "SUBFOLDERS", "EXCLUDE_DUPLICATES", "NO_PYRAMIDS", "NO_STATISTICS", "NO_THUMBNAILS", 
                   "", "NO_FORCE_SPATIAL_REFERENCE", "NO_STATISTICS", "")
            except Exception as e:
                print(e)
                pass

        print("Calculating statistics")
        arcpy.CalculateStatistics_management(mosaic_path)

        print("Building overviews now.")
        arcpy.BuildOverviews_management(mosaic_path, "", "DEFINE_MISSING_TILES", "GENERATE_OVERVIEWS", "GENERATE_MISSING_IMAGES")
    return


def find_rasters(sourcedir, pattern, keyindex):
    dl = defaultdict(list)
    globbed = glob.glob(os.path.join(sourcedir, pattern))
    for workspace in globbed:
        parts = workspace.split("\\")
        #print(parts)
        provider = parts[keyindex]
        dl[provider].append(workspace)
    return dl

# ===================================================================================
if __name__ == "__main__":
    
    import config

    MYNAME  = os.path.splitext(os.path.split(__file__)[1])[0]
    LOGFILE = MYNAME + ".log"
    logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format=config.LOGFORMAT)
    print("Writing log to %s" % LOGFILE)

    HOME = "c:\\GeoModel\\DEMbuilder"
    #       0      1          2
    # Set up the processing environment

    arcpy.env.workspace = os.path.join(HOME, "ldq.gdb")

    #county = "C:/LISdata/ccbound.shp"
    #desc = arcpy.Describe(county)
    #arcpy.env.extent = desc.extent # This causes add to mosaic to crash
    #srs = desc.spatialReference

    srs = os.path.join(HOME, "LDQ\\NAD_1983_HARN_Lambert_Conformal_Conic.prj")

    # LiDAR rasters need a slight nudge to get them to the right place!
    snappy = os.path.join(HOME, "olc_snap_raster/ogic_2011_3ft")
    arcpy.env.snapRaster = snappy

    pattern = "LDQ/LDQ-*G[345]/*/Bare*"   # Small subset for testing
    pattern = "LDQ/LDQ-*/*/Bare*"         # County-wide
    #           3  4    5  6 
    dl = find_rasters(HOME, pattern, 3)
    print(len(dl))
    
    load(dl,srs)

# That's all!
