# Eventually every project needs a config.py file.

import os

class Config(object):

    # Nothing is secret here.

    # Where the feature classes live that define the AOI
    project = os.path.join(os.environ['USERPROFILE'], 'source/repos/DEMbuilder')
    gdb = os.path.join(project, 'DEMbuilder.gdb')
    featureclasses = [
        os.path.join(gdb, 'tileindex_clatsop')
    ]

    # Local storage area for downloads and LAS files.
    repository = "F:\surface"

