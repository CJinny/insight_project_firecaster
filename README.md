# FireCaster
### *A Data Science project at [Insight Health Data Science](https://www.insighthealthdata.com/) by Jin Cui.*


[**Google Slides**](https://docs.google.com/presentation/d/1h2yOoLqJH6JAufcHWqZvux6jQl7qYj33gC5rinFcX8k/edit#slide=id.g7dd2c7fa38_3_21) * [**Web App**](http://firecaster-app.herokuapp.com/) * [**Medium**](https://medium.com/@jincui_32383/firecaster-93465e719d55) *
[**LinkedIn**](https://www.linkedin.com/in/cjinny/) * 
[**Resume**](https://drive.google.com/file/d/1XEDraiFqlYJaJL5R9kI55w_6Kfg9Nxtd/view?usp=sharing) *
[**Portfolio**](https://github.com/CJinny/portfolio)

![](https://raw.githubusercontent.com/CJinny/insight_project_firecaster/master/Image_visualization/frontpage_resize.gif)

- **Summary:** Building a deep learning model to forecast bushfire damage risk on Flinders Chase National Park using satellite imagery and weather data.
- **Keyword:** Time-Series Forecast, Computer Vision, Mixed-Data Neural Network, Remote Sensing
- **Techniques:** Keras, LSTM, CNN, GeoPandas, Rasterio, GDAL, OpenCV, BigQuery, Plotly, Dash, Heroku


## Table of Contents

- [Project Overview](#project-overview)
- [Directory Layout](#directory-layout)
- [Workflow](#workflow)
- [Results](#results)

___
### Project Overview

Flinders Chase National Park, Australia is a wildlife protection area home to many endangered species. The ongoing wildfire has devastated the Park, killing [half of its native wildlife population](https://www.cbsnews.com/news/australia-fires-nasa-satellite-images-show-wildfires-destroy-kangaroo-island/). This project attempted to establish an early warning system to forecast impending wildfire damage on Flinders Chase National Park. The data I used included: Sentinel 2A&2B satellite imagery and NOAA GSOD weather data.

___
### Directory Layout
    .
    ├── Dash_app                          # Dash web app
        ├── assets                            # base.css
        ├── data                              # Data used for web app
            ├── plot_folder                       # Matplotlib plots
        └── app.py                        # Main app file
    ├── Image_processing                  # Satellite image processing
        ├── jp2tif.py                       # Convert images from JP2 format to GeoTiff
        ├── tif2array.py                    # Resize and cropping of GeoTiff to Numpy arrays
    ├── Image_visualization               # Miscellaneous images for presentation, blog post and web apps
    ├── Model_training                    # Jupyter notebooks (Google Colab) with data preps, model training & predictions
    ├── SQL_queries_and_url_download      # BigQuery SQL queries to extract satellite image urls & gsod data, batch download
    ├── Structured_features               # Adjacency feature and gsod feature generation
    └── README.md
___
### Workflow

To build a time-series forecast model, I used data from satellite imagery from (Sentinel 2A & 2B, revisit time: 5 days) as well as NOAA global summary of the day (GSOD) weather data. The main steps of this project consists of:

- **SQL queries:** 
  1. Write SQL queries on BigQuery (Jupyter notebook on Kaggle.com) to extract URL information for satellite imagery and download data from Google Cloud Program, select only images with < 75% cloud coverage. Results were stored in csv format.
  2. Write SQL queries to extract NOAA GSOD data (also available on BigQuery).
- **Data Processing:** 
  1. Convert satellite imagery data from JP2 to GeoTiff format using GDAL, resize images using OpenCV and crop a 1000 x 1000 px region (region shown in the white box below).
  <img src="https://github.com/CJinny/insight_project_firecaster/blob/master/Dash_app/data/rgb_example.png" alt="" width=600>
  
  2. For GSOD weather data, replace missing values with median, remove features with 0 variance. repopulate missing day weather with nearest day weather.
- **Data Prep and Feature Engineering (Feature correlation shown below)**
  1. Subdivide each 1000 x 1000 region into 25 200 x 200 zones, compile images into 4-D numpy array, this is done to increase sample size and reduce image dimension.
  2. Split image data as train/valid and test based on time (2018-01-10 ~ 2020-01-15 as train/valid, 2020-01-20 ~ 2020-01-30 as test). Use KFold (K=5) method to generate train and valid set (split by zone only). The intention of the validation set was  to enable early stopping whereas the test set was to test model on independent datasets.
  3. Generate water mask using NDVI. Label burn (dNBR>0.66) areas while subtracting water mask. Count if any zone has >= 5% burn pixels => high-risk zone. 
  4. Generate adjacency features based on burn pixel % from neighbouring (8 directions) zones.
  5. Generate the series of 3 images, 3 adjacency features and 3 weather data for model training.
  
  
  
  <img src="https://github.com/CJinny/insight_project_firecaster/blob/master/Image_visualization/pearson_corr_black.png" alt="" width=600>
    
- **Model Training and Predictions**
  1. Build Keras model to incorporate series of images, series of adjacency features and series of weather data using mixed inputs (CNN and MLP), concatenate intermediate output and feed to LSTM, model diagram is shown below.
  
  <img src="https://github.com/CJinny/insight_project_firecaster/blob/master/Image_visualization/model_diagram.png" alt="" width=1000>
  
  2. Model training on each fold, create out-of-fold prediction and test-set prediction (mean prediction score from 5 models), train/valid/test strategy is shown below.
  
  <img src="https://github.com/CJinny/insight_project_firecaster/blob/master/Image_visualization/train_val_test_strategy.png" alt="" width=1000>
  
- **Data Visualization and Web App**
  1. Generate zone-risk prediction probability heatmap using seaborn.
  2. Generate Burn status (matplotlib.plt.imshow) and risk probability predictions (seaborn.heatmap) plots.
  3. Generate interactive EDA choropleth (Plotly: go.Scattergeo) and line charts (Plotly: go.Scatter).


___
### Results
 
I built a mixed-data neural network (VGG16, MLP, LSTM) to forecast wildifre damage risk and trained 5 models with a custom loss function which maximizes f4 beta score (since I want to emphasize recall, or the ability to predict a fire damage as opposed to precision, or giving false alarm). The following confusion matrix shows the validation (out-of-fold) and test set model performance.
 
<img src="https://raw.githubusercontent.com/CJinny/insight_project_firecaster/master/Image_visualization/model_performance_oof_test.png" alt="" width=600>
<img src="https://raw.githubusercontent.com/CJinny/insight_project_firecaster/master/Image_visualization/metrics.png" alt="" width=500>
  
