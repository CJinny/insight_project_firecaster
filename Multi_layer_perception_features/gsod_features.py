import pandas as pd
import numpy as np
import geopandas as gpd
import shapely
from shapely.geometry import LineString, Polygon, Polygon, Point

aus_2018 = pd.read_csv('/Users/jincui/Downloads/aus_gsod2018.csv')
aus_2019 = pd.read_csv('/Users/jincui/Downloads/aus_gsod2019.csv')
crs = {'init': 'epsg:4326'}
geometry = [Point(xy) for xy in zip(aus_2018.lon, aus_2018.lat)]
aus_2018 = gpd.GeoDataFrame(aus_2018, crs=crs, geometry=geometry)
aus_2018['date'] = pd.to_datetime(aus_2018.year*10000+aus_2018.mo*100+aus_2018.da,format='%Y%m%d')
geometry = [Point(xy) for xy in zip(aus_2019.lon, aus_2019.lat)]
aus_2019 = gpd.GeoDataFrame(aus_2019, crs=crs, geometry=geometry)
aus_2019['date'] = pd.to_datetime(aus_2019.year*10000+aus_2019.mo*100+aus_2019.da,format='%Y%m%d')
aus_records = pd.concat([aus_2018, aus_2019])



bigquery_res = pd.read_csv('/Volumes/My Passport for Mac/sentinel_2_53HPA/bigquery_results_s.csv', index_col=0)
bigquery_res['sensing_time'] = pd.to_datetime(bigquery_res['sensing_time'])
bigquery_res = bigquery_res[bigquery_res['cloud_cover']<75]
bigquery_res = bigquery_res.reset_index(drop=True)


### Flinders Chase's nearest weather station is at CAPE BORDA AWS with the stn_id 958050
local_records = aus_records[aus_records['stn']==958050]
local_records = local_records.sort_values(by='date')
local_records_s = local_records[local_records['date'].isin(bigquery_res['sensing_time'].dt.date)]


## _0: current day, _1: current day + 1 ...
local_records_day_0 = local_records[local_records['date'].isin(bigquery_res['sensing_time'].dt.date)][['date','temp','dewp','slp','visib','wdsp','mxpsd','max','min','prcp','rain_drizzle']]
local_records_day_1 = local_records[local_records['date'].isin(bigquery_res['sensing_time'].dt.date + pd.DateOffset(1))][['date','temp','dewp','slp','visib','wdsp','mxpsd','max','min','prcp','rain_drizzle']]
local_records_day_2 = local_records[local_records['date'].isin(bigquery_res['sensing_time'].dt.date + pd.DateOffset(2))][['date','temp','dewp','slp','visib','wdsp','mxpsd','max','min','prcp','rain_drizzle']]
local_records_day_3 = local_records[local_records['date'].isin(bigquery_res['sensing_time'].dt.date + pd.DateOffset(3))][['date','temp','dewp','slp','visib','wdsp','mxpsd','max','min','prcp','rain_drizzle']]
local_records_day_4 = local_records[local_records['date'].isin(bigquery_res['sensing_time'].dt.date + pd.DateOffset(4))][['date','temp','dewp','slp','visib','wdsp','mxpsd','max','min','prcp','rain_drizzle']]

## Some manual addition of data was done after generating csv, basically just to get the nearest weather data for the missing date
#local_records_day_0.to_csv('fc_day_0.csv', index=False)
#local_records_day_1.to_csv('fc_day_1.csv', index=False)
#local_records_day_2.to_csv('fc_day_2.csv', index=False)
#local_records_day_3.to_csv('fc_day_3.csv', index=False)
#local_records_day_4.to_csv('fc_day_4.csv', index=False)

local_records_day_0 = pd.read_csv('fc_day_0.csv').drop(['date'],1)
local_records_day_1 = pd.read_csv('fc_day_1.csv').drop(['date'],1)
local_records_day_2 = pd.read_csv('fc_day_2.csv').drop(['date'],1)
local_records_day_3 = pd.read_csv('fc_day_3.csv').drop(['date'],1)
local_records_day_4 = pd.read_csv('fc_day_4.csv').drop(['date'],1)


local_records_day_0.columns = [*map(lambda t: t+'_0', local_records_day_0.columns)]
local_records_day_1.columns = [*map(lambda t: t+'_1', local_records_day_1.columns)]
local_records_day_2.columns = [*map(lambda t: t+'_2', local_records_day_2.columns)]
local_records_day_3.columns = [*map(lambda t: t+'_3', local_records_day_3.columns)]
local_records_day_4.columns = [*map(lambda t: t+'_4', local_records_day_4.columns)]
gsod_5day = pd.concat([local_records_day_0, local_records_day_1, local_records_day_2, local_records_day_3, local_records_day_4], 1).drop([108])

gsod_5day.to_csv('flinders_chase_clean_5day.csv', index=False)