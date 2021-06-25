import arcpy
import os


def build_tileindex(buffer):

    workspace = os.path.join(os.environ['USERPROFILE'], 'source\\repos\\DEMbuilder', 'DEMbuilder.gdb')
    tile_folder = os.path.join(os.environ['USERPROFILE'], 'source\\repos\\DEMbuilder\\tiles')
    assert os.path.exists(tile_folder)
    county_boundary = os.path.join(workspace, "county_boundary")
    assert arcpy.Exists(county_boundary)

    arcpy.env.overwriteOutput = True

    l_fc = [
        "2015_odf_northwest",
        "or2015_usace_ncmp_astoria",
        "or2014_usace_ncmp_or",
        "or2014_metro",
        "2010_OR_USACE_Columbia_River",
        "2009_OR_DOGAMI_North_Coast",
        "2009_OLC_HoodtoCoast_8873",
        "2002_WestC",
        "west_coast2016_usgs_el_nino"
    ]

    tileindex = os.path.join(workspace, "tileindex")
    tileindex_clatsop = os.path.join(workspace, "tileindex_clatsop")

    shapefiles = []

    for f in l_fc:
        fc = os.path.join(tile_folder, f + '_index.shp')
        shapefiles.append(fc)

        assert arcpy.Exists(fc)
        try:
            arcpy.management.AddField(in_table=fc, field_name="source", field_type="TEXT", field_precision=None, field_scale=None, field_length=80, field_alias="", field_is_nullable="NULLABLE", field_is_required="NON_REQUIRED", field_domain="")
        except Exception as e:
            print("Could not add field to %s because: \"%s\"." % (f, e))

        try:
            arcpy.management.CalculateField(in_table=fc, field="source", expression='"' + f + '"', expression_type="PYTHON3", code_block="", field_type="TEXT", enforce_domains="NO_ENFORCE_DOMAINS")
        except Exception as e:
            print("Could not set field to \"%s\" because: \"%s\"." % (fc, e))

    arcpy.management.Merge(inputs=shapefiles, output=tileindex)
    selected_tiles = arcpy.management.SelectLayerByLocation(in_layer=[tileindex], overlap_type="INTERSECT", select_features=county_boundary, search_distance=buffer, selection_type="NEW_SELECTION", invert_spatial_relationship="NOT_INVERT")[0]
    arcpy.management.CopyFeatures(in_features=selected_tiles, out_feature_class=tileindex_clatsop, config_keyword="", spatial_grid_1=None, spatial_grid_2=None, spatial_grid_3=None)

if __name__ == '__main__':
    
    build_tileindex("2000 Meters")



