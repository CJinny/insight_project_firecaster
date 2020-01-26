import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt
import dash_gif_component as Gif

import numpy as np
import pandas as pd
import plotly.graph_objs as go
import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
import seaborn as sns

import flask
import glob
import os

#image_directory = './assets/'
#static_image_route = '/assets/'

image_directory = './data/plot_folder/'
static_image_route = './data/plot_folder/'


list_of_images = [os.path.basename(x) for x in glob.glob('{}plot_*.png'.format(image_directory))]
date_options = [*map(lambda t:t.split('_')[1].split('.')[0], list_of_images)]
date_options = sorted(date_options)


app = dash.Dash(__name__)


import base64

test_png = './data/plot_folder/plot_2018-01-15.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')

#test1_png = './data/plot_folder/preds_2018-01-15.png'
#test1_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')


app.layout = html.Div([
    html.H2('Select a date'),
    dcc.Dropdown(
        id='image-dropdown',
        options=[{'label': i, 'value': i} for i in date_options],
        value=date_options[0]
    ),
    html.Div([
        html.Img(
            id='image',
            src='data:image/png;base64,{}'.format(test_base64),
            style={'height' : '90%',
                'width' : '90%',
                'position' : 'relative'
            }
        ),
        
    ]),
    html.H2('To predict future wildfire damage, please upload 3 cropped Santinel images (14 bands in total, npy format) in chronological order as well the weather data (npy format) on the corresponding days'),
    
])


@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('image-dropdown', 'value')])
def update_image_src(value):
    image_path = static_image_route + 'plot_' + value + '.png'
    image_base64=base64.b64encode(open(image_path, 'rb').read()).decode('ascii') 
    #print(image_path)
    return 'data:image/png;base64,{}'.format(image_base64)




if __name__ == '__main__':
    app.run_server(debug=True)




