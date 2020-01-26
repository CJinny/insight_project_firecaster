import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

import numpy as np
import pandas as pd
import plotly.graph_objs as go
import pandas as pd
import geopandas as gpd
from matplotlib import pyplot as plt
import seaborn as sns
import base64

import flask
import glob
import os


data = gpd.read_file("data/wildfire_map_data.shp")
data['ACQ_DATE'] = pd.to_datetime(data['ACQ_DATE'])

gsod = gpd.read_file("data/aus_gsod_records_small.shp")

stn_names = np.array(gsod['name'].value_counts().index).tolist()
dropdown_options = [*map(lambda t:{'label':t, 'value': t}, stn_names)]

image_directory = './data/plot_folder/'
static_image_route = './data/plot_folder/'

list_of_images = [os.path.basename(x) for x in glob.glob('{}plot_*.png'.format(image_directory))]
date_options = [*map(lambda t:t.split('_')[1].split('.')[0], list_of_images)]
date_options = sorted(date_options)

test_png = './data/plot_folder/plot_2018-01-15.png'
test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')


model_png = './data/CNN_LSTM.png'
model_base64= base64.b64encode(open(model_png, 'rb').read()).decode('ascii')


def generate_wildfire_fig(data):

    fig = go.Figure(data=go.Scattergeo(
            lon=data['geometry'].x,
            lat=data['geometry'].y,
            mode='markers',
            text=data['text'],
            marker=dict(
                size=3, opacity=0.8,
                reversescale=True, autocolorscale=False,
                line=dict(width=0),
                colorscale='Inferno',
                cmin=500,
                cmax=5000,
                color=data['FRP'],
                colorbar_title='Radiative Power'
                )
            ),
            layout=dict(
                geo=dict(
                    lataxis=dict(range=[-44,-10.5]),
                    lonaxis=dict(range=[113,154])
                    )
                
            )           
    )
    #fig.update_layout(plot_bgcolor='#F5EEF8')
    return fig

def generate_gsod_fig(data):
    return go.Figure(data=go.Scattergeo(
        lon=data['geometry'].x,
        lat=data['geometry'].y,
        mode='markers',
        text=data['text'],
        marker=dict(
            size=data['wdsp'].map(lambda t:np.sqrt(t).round()+1),
            opacity=0.8,
            reversescale=True, autocolorscale=False,
            line=dict(width=0),
            colorscale='Inferno',
            cmin=data['temp'].min(),
            cmax=data['temp'].max(),
            #cmax=test['FRP'].max(),
            color=data['temp'],
            colorbar_title='Mean temperature (\u00B0F)'
            )
        ),
        layout=dict(
              geo=dict(
                lataxis=dict(range=[-44,-10.5]),
                lonaxis=dict(range=[113,154])
                ),
            #title_text='GSOD measurements'  
        )           
    )



external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True

index_page = html.Div([
    dcc.Link('Map visualization', href='/page-1'),
    html.Br(),
    dcc.Link('Images and prediction', href='/page-2'),
    html.Br(),
    dcc.Link('Model architecture', href='/page-3'),
    html.Br(),
    html.Br(),
])



app.layout = html.Div([
    html.H2('Firecaster'),
    dcc.Location(id='url', refresh=False),
    index_page,
    html.Div(id='page-content')
])




page_1_layout = html.Div(
                    style={'backgroundColor': 'white'},
                    children = [
                        html.Div([
                            html.Br(),
                            html.H5('Australian wildfire distribution\nbased on NASA FIRMS data'),
                            html.H6(
                                children='Select date range',
                                style={'textAlign': 'left', 'color': 'black'}
                            ),
                            dcc.DatePickerRange(
                                id="wildfire-date-range-slider",
                                month_format='MMM Do, YY',
                                start_date=dt(2018,1,1),
                                end_date=dt(2020,1,16)
                            ),
                            html.Br(),
                            html.H6(
                                children='Select sensor',
                                style={'textAlign': 'left', 'color': 'black'}
                            ),
                            dcc.Dropdown(
                                id="wildfire-sensor-checklist",
                                options=[
                                    {'label': 'MODIS', 'value': 'MODIS'},
                                    {'label': 'VIIRS', 'value': 'VIIRS'}
                                ],
                                value=['MODIS','VIIRS'],
                                multi=True
                            ),
                            html.Br(),
                            html.H6(
                                children='Filter wildfire by fire radiant power (FRP)',
                                style={'textAlign': 'left','color': 'black'}
                            ),
                            dcc.RangeSlider(
                                id="wildfire-frp-rangeslider",
                                marks={i: '{}'.format(i) for i in range(500, 23500, 3000)},
                                min=500,
                                max=23500,
                                value=[500, 23500]
                            ),
                            html.Div([
                                dcc.Graph(
                                id="wildfire-map"
                                )
                            ])
                        ],style={'backgroundColor':'#F5EEF8', 'width': '49%', 'float':'left'}),
                        html.Div([
                            html.Br(),
                            html.H5('Ground surface summary of the day based on NOAA GSOD data'),
                            html.H6(
                                children='Select date range',
                                style={'textAlign': 'left', 'color': 'black'}
                            ),
                            dcc.DatePickerRange(
                                id="gsod-range-slider",
                                month_format='MMM Do, YY',
                                start_date=dt(2019,12,16),
                                end_date=dt(2020,1,16)
                            ),
                            
                            html.Div([
                                dcc.Graph(
                                id="gsod-map"
                                )
                            ]),html.Div(id='test')
                        ],style={'backgroundColor':'AliceBlue', 'width':'49%', 'float':'right'})    
                ])

@app.callback(
    dash.dependencies.Output('wildfire-map', 'figure'),
    [dash.dependencies.Input('wildfire-date-range-slider', 'start_date'),
     dash.dependencies.Input('wildfire-date-range-slider', 'end_date'),
     dash.dependencies.Input('wildfire-sensor-checklist', 'value'),
     dash.dependencies.Input('wildfire-frp-rangeslider', 'value')
     ]
)
def update_wildfire(start_date, end_date, checklist, rangeslider):
    idx = list(data[(data['ACQ_DATE'] <= end_date) & (data['ACQ_DATE'] >= start_date)].index)
    data_subset = data.iloc[idx,:]
    data_subset = data_subset[data_subset['INSTRUMENT'].isin(checklist)]

    data_subset = data_subset[(data_subset['FRP']<=rangeslider[1]) & (data_subset['FRP']>=rangeslider[0])]
    return generate_wildfire_fig(data_subset)


@app.callback(
     dash.dependencies.Output('gsod-map', 'figure'),
     [dash.dependencies.Input('gsod-range-slider', 'start_date'),
      dash.dependencies.Input('gsod-range-slider', 'end_date'),
     ]
)
def update_gsod(start_date, end_date):
    idx = list(gsod[(gsod['date'] <= end_date) & (gsod['date'] >= start_date)].index)
    gsod_subset = gsod.iloc[idx,:]
    return generate_gsod_fig(gsod_subset)


page_2_layout = html.Div([
                    html.H3('Satellite images and model prediction'),
                    html.H4('Select a date'),
                    html.P("Predictions start on 2018-02-14"),
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
                    
                ])


@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('image-dropdown', 'value')])
def update_image_src(value):
    image_path = static_image_route + 'plot_' + value + '.png'
    image_base64=base64.b64encode(open(image_path, 'rb').read()).decode('ascii') 
    #print(image_path)
    return 'data:image/png;base64,{}'.format(image_base64)



page_3_layout = html.Div([
                    html.Img(
                        id='model',
                        src='data:image/png;base64,{}'.format(model_base64),
                        style={'height' : '90%',
                               'width' : '90%',
                               'position' : 'relative'}
                    )
                ])



@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        pass
        #return index_page



if __name__ == '__main__':
    app.run_server(debug=True)
