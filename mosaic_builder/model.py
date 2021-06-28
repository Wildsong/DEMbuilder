# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# model.py
# Created on: 2018-07-31 08:43:43.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Set the necessary product code
import arcinfo


# Import arcpy module
import arcpy


# Local variables:
T2009_OLC_Willamette_Valley = "C:\\GeoModel\\DEMbuilder\\ldq.gdb\\T2009_OLC_Willamette_Valley"
T2009_OLC_Willamette_Valley__2_ = T2009_OLC_Willamette_Valley
Bare_Earth = "C:\\GeoModel\\DEMbuilder\\LDQ\\LDQ-45123G3\\2009_OLC_Hood to Coast\\Bare_Earth"

# Process: Add Rasters To Mosaic Dataset
arcpy.AddRastersToMosaicDataset_management(T2009_OLC_Willamette_Valley, "Raster Dataset", "'C:\\GeoModel\\DEMbuilder\\LDQ\\LDQ-45123G3\\2009_OLC_Hood to Coast\\Bare_Earth'", "UPDATE_CELL_SIZES", "UPDATE_BOUNDARY", "NO_OVERVIEWS", "", "0", "1500", "", "", "SUBFOLDERS", "ALLOW_DUPLICATES", "NO_PYRAMIDS", "NO_STATISTICS", "NO_THUMBNAILS", "", "NO_FORCE_SPATIAL_REFERENCE", "NO_STATISTICS", "")

