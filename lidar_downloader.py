"""
Using a feature class to define a list of downloads, do the downloads.

Created 2018-05-18 Brian Wilson <bwilson@co.clatsop.or.us>
"""
import os
import arcpy
import logging
import requests
from config import Config

errors = []

def download(name, url, output_folder):
    """
    We're assuming here that CWD is the base path for output.
    """
    target = os.path.join(output_folder, name)

    # It should also be possible to check the file size
    # and look at the header returned from the server
    # to see if the existing file was completely downloaded
    # Go look in the downloader log, you will see header messages
    # like this
    # 2021-06-25 10:13:13,660 https://chs.coast.noaa.gov:443 "GET /htdata/lidar2_z/geoid18/data/6379/CLATSOP/20160209_45123H5111.laz HTTP/1.1" 200 131762452
    # so I think you could ask the server for the file size before 
    # transferring it.

    if os.path.exists(target):
        logging.info("Already have %s" % target)
        return

    # If the name starts with a path spec then create the path
    path, filename = os.path.split(target)
    if path:
        os.makedirs(path, exist_ok=True)
    
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(target, 'wb') as fp:
                for chunk in r.iter_content(chunk_size=8192):
                    fp.write(chunk)
    except IOError as e:
        print("Download failed with", e)
        errors.append(url)
        if os.path.exists(target):
            os.unlink(target)
            print("Removed partial download of %s" % target)
        logging.error("Error: %s %s" % (name, e))
    return

def read_fc(fc):
#    fields = ["Title", "links", "DataType", "collectionyear", "qualitylevel"]
    fields = ['Name', 'URL', 'source']

    total = int(arcpy.management.GetCount(fc)[0])
    count = 0
    total_downloaded = 0
    skipped = 0

    with arcpy.da.SearchCursor(fc, fields) as cursor:
        for row in cursor:
            #print(row)
            #title = row[0]
            #links = row[1]
            name    = row[0].strip()
            url     = row[1].strip()
            source  = row[2].strip()

            count += 1
            downloaded = download(name, url, source)
            if downloaded: 
                print("%d/%d %s" % (count, total, name))
                total_downloaded += 1
            else:
                skipped += 1

    return total_downloaded, skipped

# ============================================================================
if __name__ == "__main__":

    MYNAME  = os.path.splitext(os.path.split(__file__)[1])[0]
    LOGFILE = MYNAME + ".log"
    LOGFORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format=LOGFORMAT)
    print("Writing log to %s." % LOGFILE)
    logging.info("Starting download run. ====================")

    # Files will be downloaded into the current working directory.
    downloads = os.path.join(Config.repository, "downloads")
    os.chdir(downloads)

    for fc in Config.featureclasses:
        if arcpy.Exists(fc):
            print(fc)
        (downloaded, skipped) = read_fc(fc)

    logging.info("We're done! =====================")
    print("Downloaded %d, already had %d." % (downloaded, skipped))
    if len(errors): print(errors)

# That's all!
