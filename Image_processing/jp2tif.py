'''
Recursively convert Sentinel images from JP2 format to TIF format
'''

#### Encountered some package installation problems while using geopandas, so i ccreated a conda env called "TEST"
## conda create --name TEST python=3.7 geopandas
## conda ativate test

import glob
import subprocess

inpaths_b01 = glob.glob('S2*/GRANULE/L*/IMG_DATA/*B01.jp2')
inpaths_b02 = glob.glob('S2*/GRANULE/L*/IMG_DATA/*B02.jp2')
inpaths_b03 = glob.glob('S2*/GRANULE/L*/IMG_DATA/*B03.jp2')
inpaths_b04 = glob.glob('S2*/GRANULE/L*/IMG_DATA/*B04.jp2')
inpaths_b05 = glob.glob('S2*/GRANULE/L*/IMG_DATA/*B05.jp2')
inpaths_b06 = glob.glob('S2*/GRANULE/L*/IMG_DATA/*B06.jp2')
inpaths_b07 = glob.glob('S2*/GRANULE/L*/IMG_DATA/*B07.jp2')
inpaths_b08 = glob.glob('S2*/GRANULE/L*/IMG_DATA/*B08.jp2')
inpaths_b8A = glob.glob('S2*/GRANULE/L*/IMG_DATA/*B8A.jp2')
inpaths_b09 = glob.glob('S2*/GRANULE/L*/IMG_DATA/*B09.jp2')
inpaths_b10 = glob.glob('S2*/GRANULE/L*/IMG_DATA/*B10.jp2')
inpaths_b11 = glob.glob('S2*/GRANULE/L*/IMG_DATA/*B11.jp2')
inpaths_b12 = glob.glob('S2*/GRANULE/L*/IMG_DATA/*B12.jp2')
inpaths_tci = glob.glob('S2*/GRANULE/L*/IMG_DATA/*TCI.jp2')


outpaths = [*map(lambda t:t.split('/')[-3], inpaths_b01)]

for i in range(len(inpaths_b01)):
    outpath = outpaths[i]
    existing_files = glob.glob('L1C*_b01.tif')
    if f"{outpath}_b01.tif" in existing_files:
        print("pass")
        pass
    else:
        try:
            subprocess.run(f"gdal_translate -of GTiff {inpaths_b01[i]} {outpath}_b01.tif", shell=True, check=True)
        except Exception:
            print(inpath_b01[i])

for i in range(len(inpaths_b02)):
    outpath = outpaths[i]
    existing_files = glob.glob('L1C*_b02.tif')
    if f"{outpath}_b02.tif" in existing_files:
        print("pass")
        pass
    else:
        try:
            subprocess.run(f"gdal_translate -of GTiff {inpaths_b02[i]} {outpath}_b02.tif", shell=True, check=True)
        except Exception:
            print(inpath_b01[i])

for i in range(len(inpaths_b03)):
    outpath = outpaths[i]
    existing_files = glob.glob('L1C*_b03.tif')
    if f"{outpath}_b03.tif" in existing_files:
        print("pass")
        pass
    else:
        try:
            subprocess.run(f"gdal_translate -of GTiff {inpaths_b03[i]} {outpath}_b03.tif", shell=True, check=True)
        except Exception:
            print(inpath_b01[i])


for i in range(len(inpaths_b04)):
    outpath = outpaths[i]
    existing_files = glob.glob('L1C*_b04.tif')
    if f"{outpath}_b04.tif" in existing_files:
        print("pass")
        pass
    else:
        try:
            subprocess.run(f"gdal_translate -of GTiff {inpaths_b04[i]} {outpath}_b04.tif", shell=True, check=True)
        except Exception:
            print(inpath_b04[i])

for i in range(len(inpaths_b05)):
    outpath = outpaths[i]
    existing_files = glob.glob('L1C*_b05.tif')
    if f"{outpath}_b05.tif" in existing_files:
        print("pass")
        pass
    else:
        try:
            subprocess.run(f"gdal_translate -of GTiff {inpaths_b05[i]} {outpath}_b05.tif", shell=True, check=True)
        except Exception:
            print(inpath_b05[i])

for i in range(len(inpaths_b06)):
    outpath = outpaths[i]
    existing_files = glob.glob('L1C*_b06.tif')
    if f"{outpath}_b06.tif" in existing_files:
        print("pass")
        pass
    else:
        try:
            subprocess.run(f"gdal_translate -of GTiff {inpaths_b06[i]} {outpath}_b06.tif", shell=True, check=True)
        except Exception:
            print(inpath_b06[i])

for i in range(len(inpaths_b07)):
    outpath = outpaths[i]
    existing_files = glob.glob('L1C*_b07.tif')
    if f"{outpath}_b07.tif" in existing_files:
        print("pass")
        pass
    else:
        try:
            subprocess.run(f"gdal_translate -of GTiff {inpaths_b07[i]} {outpath}_b07.tif", shell=True, check=True)
        except Exception:
            print(inpath_b07[i])

for i in range(len(inpaths_b08)):
    outpath = outpaths[i]
    existing_files = glob.glob('L1C*_b08.tif')
    if f"{outpath}_b08.tif" in existing_files:
        print("pass")
        pass
    else:
        try:
            subprocess.run(f"gdal_translate -of GTiff {inpaths_b08[i]} {outpath}_b08.tif", shell=True, check=True)
        except Exception:
            print(inpath_b08[i])

for i in range(len(inpaths_b8A)):
    outpath = outpaths[i]
    existing_files = glob.glob('L1C*_b8A.tif')
    if f"{outpath}_b8A.tif" in existing_files:
        print("pass")
        pass
    else:
        try:
            subprocess.run(f"gdal_translate -of GTiff {inpaths_b8A[i]} {outpath}_b8A.tif", shell=True, check=True)
        except Exception:
            print(inpath_b8A[i])

for i in range(len(inpaths_b09)):
    outpath = outpaths[i]
    existing_files = glob.glob('L1C*_b09.tif')
    if f"{outpath}_b09.tif" in existing_files:
        print("pass")
        pass
    else:
        try:
            subprocess.run(f"gdal_translate -of GTiff {inpaths_b09[i]} {outpath}_b09.tif", shell=True, check=True)
        except Exception:
            print(inpath_b09[i])

for i in range(len(inpaths_b10)):
    outpath = outpaths[i]
    existing_files = glob.glob('L1C*_b10.tif')
    if f"{outpath}_b10.tif" in existing_files:
        print("pass")
        pass
    else:
        try:
            subprocess.run(f"gdal_translate -of GTiff {inpaths_b10[i]} {outpath}_b10.tif", shell=True, check=True)
        except Exception:
            print(inpath_b10[i])

for i in range(len(inpaths_b11)):
    outpath = outpaths[i]
    existing_files = glob.glob('L1C*_b11.tif')
    if f"{outpath}_b11.tif" in existing_files:
        print("pass")
        pass
    else:
        try:
            subprocess.run(f"gdal_translate -of GTiff {inpaths_b11[i]} {outpath}_b11.tif", shell=True, check=True)
        except Exception:
            print(inpath_b11[i])

for i in range(len(inpaths_b12)):
    outpath = outpaths[i]
    existing_files = glob.glob('L1C*_b12.tif')
    if f"{outpath}_b12.tif" in existing_files:
        print("pass")
        pass