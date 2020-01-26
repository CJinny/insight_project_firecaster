'''
Recursively convert TIF images to numpy array with some cropping and resizing
'''

import numpy as np
import pandas as pd
import gc
import os
from matplotlib import pyplot as plt
import rasterio
import geopandas as gpd
from rasterio.plot import show, show_hist
import rasterio
import rasterio.mask as Mask
import rasterio.features
import rasterio.warp
from rasterio.plot import show_hist
import fiona
import os
import glob
import shapely
from shapely.geometry import LineString, Polygon, Polygon, Point, MultiPoint, MultiPolygon
from functools import partial
import pyproj
import shapely
from shapely.ops import transform
from tqdm import tqdm_notebook, tqdm
## help with figure rotation
from scipy import ndimage, misc
from shapely.geometry import Point
import geopandas as gpd
import cv2   # usse to resize images so that every image would have the same size!!!! 
## GDAL_DATA environment problem
os.environ['GDAL_DATA'] = '/opt/anaconda3/pkgs/libgdal-2.3.3-h0950a36_0/share/gdal'
fiona.drvsupport.supported_drivers['kml'] = 'rw'
fiona.drvsupport.supported_drivers['KML'] = 'rw'
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib_scalebar.scalebar import ScaleBar


bigquery_res = pd.read_csv('/Volumes/My Passport for Mac/sentinel_2_53HPA/bigquery_results_s.csv', index_col=0)


def concat_bands(name='L1C_T53HPA_A004418_20180110T005319', 
                 BASE = '/Volumes/My Passport for Mac/sentinel_2_53HPA/',
                 #OUT='/Volumes/My Passport for Mac/'
                 ):
    '''Resize all bands to (5490, 5490), resolution at 20meter/pixel'''

    b01 = rasterio.open(BASE+name+'_b01.tif').read(1)
    b01 = np.expand_dims(cv2.resize(b01, (5490,5490)), axis=2)[3000:4000,2200:3200,:]
    b09 = rasterio.open(BASE+name+'_b09.tif').read(1)
    b09 = np.expand_dims(cv2.resize(b09, (5490,5490)), axis=2)[3000:4000,2200:3200,:]
    b10 = rasterio.open(BASE+name+'_b10.tif').read(1)
    b10 = np.expand_dims(cv2.resize(b10, (5490,5490)), axis=2)[3000:4000,2200:3200,:]

    b02 = rasterio.open(BASE+name+'_b02.tif').read(1)
    b02 = np.expand_dims(cv2.resize(b02, (5490,5490)), axis=2)[3000:4000,2200:3200,:]
    b03 = rasterio.open(BASE+name+'_b03.tif').read(1)
    b03 = np.expand_dims(cv2.resize(b03, (5490,5490)), axis=2)[3000:4000,2200:3200,:]
    b04 = rasterio.open(BASE+name+'_b04.tif').read(1)
    b04 = np.expand_dims(cv2.resize(b04, (5490,5490)), axis=2)[3000:4000,2200:3200,:]
    b08 = rasterio.open(BASE+name+'_b08.tif').read(1)
    b08 = np.expand_dims(cv2.resize(b08, (5490,5490)), axis=2)[3000:4000,2200:3200,:]
    tci = rasterio.open(BASE+name+'_tci.tif').read(1)
    tci = np.expand_dims(cv2.resize(tci, (5490,5490)), axis=2)[3000:4000,2200:3200,:]

    b05 = np.expand_dims(rasterio.open(BASE+name+'_b05.tif').read(1), axis=2)[3000:4000,2200:3200,:]
    b06 = np.expand_dims(rasterio.open(BASE+name+'_b06.tif').read(1), axis=2)[3000:4000,2200:3200,:]
    b07 = np.expand_dims(rasterio.open(BASE+name+'_b07.tif').read(1), axis=2)[3000:4000,2200:3200,:]
    b8A = np.expand_dims(rasterio.open(BASE+name+'_b8A.tif').read(1), axis=2)[3000:4000,2200:3200,:]
    b11 = np.expand_dims(rasterio.open(BASE+name+'_b11.tif').read(1), axis=2)[3000:4000,2200:3200,:]
    b12 = np.expand_dims(rasterio.open(BASE+name+'_b12.tif').read(1), axis=2)[3000:4000,2200:3200,:]
    
    concat = np.concatenate([b01,b02,b03,b04,b05,b06,b07,b08,b09,b10,b11,b12,b8A,tci],axis=-1)
    concat = np.expand_dims(concat, 0)
    return concat


for i in tqdm_notebook(range(1, len(bigquery_res['granule_id'].values))):
    if i == 0:
        imgs = concat_bands(bigquery_res['granule_id'].values[i])
    else:
        imgs = np.concatenate([res, concat_bands(bigquery_res['granule_id'].values[i])])


# A smooth value is added to avoid ZeroDivision error!
smooth = 1e-5
b04 = imgs[:,:,:,3:4]
b08 = imgs[:,:,:,7:8]
b12 = imgs[:,:,:,11:12]

nbr = (b08-b12+smooth)/(b08+b12+smooth)
dnbr = np.zeros((nbr.shape[0]-1, nbr.shape[1], nbr.shape[2], nbr.shape[3]))
for i in range(len(dnbr)):
    dnbr[i,:] = nbr[i+1,:] - nbr[i,:]

### need water mask before model training
np.savez_compressed('../cloud_control_data.npz', dnbr=dnbr, nbr=nbr)
