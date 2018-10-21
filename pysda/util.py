# -*- encoding: utf-8 -*-
import os
import numpy as np
import zipfile

def check_dir(apath):
    dirname = os.path.dirname(apath)
    if not os.path.isdir(dirname):
        os.makedirs(dirname)

def get_dist(pt0, pt1):
    x0, y0 = pt0
    x1, y1 = pt1
    d = np.sqrt((x1-x0)**2+(y1-y0)**2)
    return d

def zip_shp(fp):
    zfs = os.listdir(os.path.dirname(fp))
    fbase = os.path.basename(fp)[:-4]
    zfs2 = [ f for f in zfs if f[:len(fbase)]==fbase ]
    zipf = zipfile.ZipFile(fp,'w')
    for f in zfs2:
        if f[-4:]!='.zip':
            #print f
            fn2 = os.path.join(os.path.dirname(fp), f)
            zipf.write(fn2, os.path.basename(fn2))
    zipf.close()
