"""
$project$ common configuration properties
@author: bwilson
@date:   7/30/2018 12:18:11 PM
"""
import os
LOGFORMAT = '%(asctime)s %(message)s'

GIS_FILESERVER  = "\\\\clatsop.co.clatsop.or.us\\Data\\Applications\\GIS" # Normally mapped as the "K:"
LISDATA         = os.path.join(GIS_FILESERVER, "LISData")
LOCAL_GDB       = "C:\\GeoModel\\AGE_maintenance\\DataLoader\\DataLoader.gdb"
ENTERPRISE_GDB     = os.path.join(GIS_FILESERVER, "ORMAP_CONVERSION\\scripts\\connections\\cc-gis.sde")
ENTERPRISE_SANDBOX = os.path.join(GIS_FILESERVER, "ORMAP_CONVERSION\\scripts\\connections\\cc-gis_sandbox.sde")
