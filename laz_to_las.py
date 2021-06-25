"""
Find all the LAZ files that need to be
decompressed and then push them one at a time to laszip.exe
"""
import os
import logging
import subprocess
from config import Config

laszip = os.path.join(os.getcwd(), 'laszip-cli.exe')

def decompress(sourcefile, destfolder):
    logging.info("Decompress %s" % sourcefile)
    cmd = [laszip, '-i', sourcefile, '-odir', destfolder, "-cores", '4']
    try:
        print(cmd)
        #subprocess.run(cmd)
    except Exception as e:
        logging.error("Decompress FAILED for %s. %s" % (sourcefile,e))
        # maybe delete file here???
        return False
    return True

def check(file):
    cmd = [laszip, '-i', file, '-check']
    try:
        result = subprocess.run(cmd, capture_output=True)
    except Exception as e:
        print('Check failed for %s: %s' % (file, e))
        return False
    return result.stderr.startswith(b'SUCCESS')

# ============================================================================
if __name__ == "__main__":

    MYNAME  = os.path.splitext(os.path.split(__file__)[1])[0]
    LOGFILE = MYNAME + ".log"
    LOGFORMAT = '%(asctime)s %(message)s'
    logging.basicConfig(filename=LOGFILE, level=logging.DEBUG, format=LOGFORMAT)
    print("Writing log to %s." % LOGFILE)
    logging.info("Starting decompress run. ====================")

    downloads = os.path.join(Config.repository, "downloads")
    os.chdir(downloads)

    count = 0
    skipped = 0

    broken_laz = []
    broken_las = []

    for root,dirs,files in os.walk('.'):
        for f in files:
            sourcefile = os.path.join(root, f)
            folder = root[2:]
            name, ext = os.path.splitext(f)
            destfolder = os.path.join('..', "lidar", folder)
            destfile = os.path.join(destfolder, name + '.las')
            if os.path.exists(destfile):
                if not check(destfile):
                    broken_las.append(destfile)
                    logging.info("Check failed for %s." % destfile)
                else:
                    logging.info("We already have %s, skipping decompress." % destfile)
                    skipped += 1
            else:
                if not check(sourcefile):
                    broken_laz.append(sourcefile)
                    logging.info("Check failed for %s." % sourcefile)
                else:
                    os.makedirs(destfolder, exist_ok=True)
                    if decompress(sourcefile, destfolder):
                        count += 1

    logging.info("We're done! =====================")
    print("We're done! %d decompressed %d skipped." % (count, skipped))

# That's all!
