import dash
import dash_core_components as dcc
import dash_html_components as html
import datetime
import numpy as np
import pandas as pd
import plotly.graph_objs as go
import pandas as pd
import geopandas as gpd
import base64
import glob
import os


data = gpd.read_file("data/wildfire_map_data.shp")
data['ACQ_DATE'] = pd.to_datetime(data['ACQ_DATE'])

gsod = gpd.read_file("data/aus_gsod_records_small.shp")
#gsod['dewp'] = gsod['dewp'].astype(float)             # needed if you wanna plot dewp


stn_names = np.array(gsod['name'].value_counts().index).tolist()
dropdown_options = [*map(lambda t:{'label':t, 'value': t}, stn_names)]

image_directory = './data/plot_folder/'
static_image_route = './data/plot_folder/'

list_of_images = [os.path.basename(x) for x in glob.glob('{}plot_*.png'.format(image_directory))]
date_options = [*map(lambda t:t.split('_')[1].split('.')[0], list_of_images)]
date_options = sorted(date_options,  reverse=True)

#test_png = './data/plot_folder/plot_2019-12-31.png'
test_png = './data/plot_folder/plot_2020-01-25.png'

test_base64 = base64.b64encode(open(test_png, 'rb').read()).decode('ascii')


model_png = './data/CNN_LSTM.png'
model_base64= base64.b64encode(open(model_png, 'rb').read()).decode('ascii')

rgb_png = './data/rgb_example.png'
rgb_base64= base64.b64encode(open(rgb_png, 'rb').read()).decode('ascii')



def generate_wildfire_fig(data):

    return go.Figure(data=go.Scattergeo(
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
                    ),
                width=620, height=600
                
            )           
    )

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

def plot_frp(data):
    agg = data.groupby('ACQ_DATE').agg({'FRP':[max]})
    agg = agg.reset_index()
    agg.columns = ['ACQ_DATE','MAX_FRP']
    trace = go.Scatter(
        x=agg['ACQ_DATE'], y=agg['MAX_FRP'],
        mode='lines+markers', marker=dict(size=3)
    )
    layout = go.Layout(
        title='Maximum FRP by date',
        xaxis_title='Date', yaxis_title='Maximum FRP',
        plot_bgcolor='white', 
    )
    return go.Figure(data=trace, layout=layout)

def generate_gsod_temp_plot(gsod_data):
    agg = gsod_data.groupby(['name','date']).agg({'temp':np.mean})
    agg = agg.reset_index(drop=False)                                    
    stn_names = list(agg['name'].value_counts().index)

    traces = []
    for i in range(len(stn_names)):
        data = agg[agg['name']==stn_names[i]].sort_values(by='date')
        traces.append(go.Scatter(x=data['date'], y=data['temp'], name=stn_names[i], mode='lines+markers'))
    layout = go.Layout(
        title='Mean temperature (\u00B0F) by date',
        xaxis_title='Date', yaxis_title='Temperature (\u00B0F)', plot_bgcolor='white', 
        width=800, height=350,
    )
    return go.Figure(data=traces, layout=layout)

def generate_gsod_wdsp_plot(gsod_data):
    agg = gsod_data.groupby(['name','date']).agg({'wdsp':np.mean})
    agg = agg.reset_index(drop=False)
                                    
    stn_names = list(agg['name'].value_counts().index)
    traces = []
    for i in range(len(stn_names)):
        data = agg[agg['name']==stn_names[i]].sort_values(by='date')
        traces.append(go.Scatter(x=data['date'], y=data['wdsp'], name=stn_names[i], mode='lines+markers'))
    layout = go.Layout(
        title='Mean wind speed (knots) by date',
        xaxis_title='Date', yaxis_title='Wind speed (knots)', plot_bgcolor='white', 
        width=800, height=350,
    )
    return go.Figure(data=traces, layout=layout)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


server = app.server

app.config.suppress_callback_exceptions = True

index_page = html.Div([
    dcc.Link('About', href='/page-0'),
    html.Br(),
    dcc.Link('Satellite images and model prediction', href='/page-1'),
    html.Br(),
    dcc.Link('Model architecture', href='/page-2'),
    html.Br(),
    dcc.Link('Australian wildfire and weather visualization', href='/page-3'),
    html.Br(),
    html.Br(),
], style={'fontSize': '120%'})



app.layout = html.Div([
    html.Div([
        html.H1('Firecaster', style={'font-weight': 'bold'}),
        html.H4('Helping animal rescue team forecast wildfire damage risk'),
    ], style={'textAlign':'center'}),
    
    
    dcc.Location(id='url', refresh=False),
    index_page,
    html.Div(id='page-content')
])



page_0_layout = html.Div([
                    html.Div([
                        html.H4('Background', style={'font-weight': 'bold'}),
                        html.P(
                            [
                                """
                                Firecaster is a Dash-based web application that helps forecast fire damage risk on parts of Flinders Chase National Park, Australia using Sentinel satellite imagery as well NOAA global summary of the day (gsod) weather data.
                                The scope of this project focuses on a 20km x 20km (1000px x 1000px) bushland region. The region was then subdivided into 25 4km x 4km sectors. 
                                I used difference normalized burn ratio (dNBR) to determine burn severity of a pixel, with a cut-off of 0.66 (high severity if dNBR > 0.66, low severity otherwise). For more information about dNBR and wildfire damage classification, please check
                                """,
                                html.A("here.", href="https://www.earthdatascience.org/courses/earth-analytics/multispectral-remote-sensing-modis/normalized-burn-index-dNBR/"),
                            ]
                        ),
                        html.P(
                            [
                                """
                                I then classify sectors with equal or more than 5% pixels in high severity category as high risk sectors. 
                                Predicted Models were then constructed using Keras and trained on Google Colab to classify if a sector will become high-risk region or not in the coming 5 days. 
                                The model takes input of 3 time-series 200x200 pixel images as well as their corresponding adjacency features and gsod weather data. For additional information on feature engineering & model training, 
                                please visit my
                                """,
                                html.A("GitHub repository.", href="https://github.com/CJinny/insight_project_firecaster"),
                            ]
                        ),
                        html.P(
                            [
                                """
                                This project was completed in 3 weeks as part of the 
                                """,
                                html.A("Insight Health Data Science Program.", href="https://www.insighthealthdata.com/"),
                                html.Br(),
                                html.Br(),
                                """
                                Jin Cui
                                """,
                                html.Br(),
                                html.A("GitHub", href="https://github.com/CJinny"),
                                html.Br(),
                                html.A("LinkedIn", href="https://www.linkedin.com/in/jin-cui-14379ba1/"),
                                html.Br(),
                                html.A("Portfolio", href="https://cjinny.github.io/portfolio/"),
                            ]
                        ),
                    ],style={'width':'44%', 'float':'left'}),
                    html.Div([
                            html.Img(
                            id='rgb',
                            src='data:image/png;base64,{}'.format(rgb_base64),
                            style={'height' : '50%',
                                'width' : '50%',
                                }
                        ),
                        
                    ]),
                ])

page_1_layout = html.Div([
                    html.H3('Images and model prediction'),
                    html.P("Out-of-fold valid-set predictions start on 2018-02-14, test-set predictions start on 2020-01-20"),
                    #html.Br(),
                    #html.Br(),
                    html.H4('Select a date'),
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

page_2_layout = html.Div([
                    html.Img(
                        id='model',
                        src='data:image/png;base64,{}'.format(model_base64),
                        style={'height' : '200%',
                               'width' : '200%',
                               'position' : 'relative'}
                    )
                ])

page_3_layout = html.Div(
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
                                start_date=datetime.datetime(2018,1,1),
                                end_date=datetime.datetime(2020,1,16)
                            ),
                            html.Br(),
                            html.H6(
                                children='Select sensor',
                                style={'textAlign': 'left', 'color': 'black'}
                            ),
                            dcc.Dropdown(
                                id="wildfire-sensor-dropdown",
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
                                ),
                                dcc.Graph(
                                    id='wildfire-frp-plot'
                                )
                            ])
                        ],style={'width': '45%', 'float':'left'}),
                        html.Div([
                            html.Br(),
                            html.H5('Weather data based on NOAA GSOD data'),
                            html.H6(
                                children='Select date range',
                                style={'textAlign': 'left', 'color': 'black'}
                            ),
                            dcc.DatePickerRange(
                                id="gsod-range-slider",
                                month_format='MMM Do, YY',
                                start_date=datetime.datetime(2019,12,16),
                                end_date=datetime.datetime(2020,1,16)
                            ),
                            
                            html.Div([
                                dcc.Graph(
                                    id="gsod-map"
                                )
                            ]),
                            html.Div([
                                html.H6(
                                    children='Select station(s) for GSOD data',
                                    style={'textAlign': 'left', 'color': 'black'}
                                ),
                                dcc.Dropdown(
                                    id="gsod-station-dropdown",
                                    options=dropdown_options,
                                    value=['CAPE BORDA AWS', 'PORT LINCOLN'],
                                    multi=True
                                ),
                                dcc.Graph(
                                    id='gsod-temp-plot'
                                ),
                                dcc.Graph(
                                    id='gsod-wdsp-plot'
                                )
                            ])

                        ],style={'width':'45%', 'float':'right'})    
                ])

@app.callback(
    # add line plot showing maximum FRP
    [dash.dependencies.Output('wildfire-map', 'figure'),
    dash.dependencies.Output('wildfire-frp-plot', 'figure'),
    ],
    [dash.dependencies.Input('wildfire-date-range-slider', 'start_date'),
     dash.dependencies.Input('wildfire-date-range-slider', 'end_date'),
     dash.dependencies.Input('wildfire-sensor-dropdown', 'value'),
     dash.dependencies.Input('wildfire-frp-rangeslider', 'value')
     ]
)
def update_wildfire(start_date, end_date, checklist, rangeslider):
    idx = list(data[(data['ACQ_DATE'] <= end_date) & (data['ACQ_DATE'] >= start_date)].index)
    data_subset = data.iloc[idx,:]
    data_subset = data_subset[data_subset['INSTRUMENT'].isin(checklist)]

    data_subset = data_subset[(data_subset['FRP']<=rangeslider[1]) & (data_subset['FRP']>=rangeslider[0])]
    return generate_wildfire_fig(data_subset), plot_frp(data_subset)


@app.callback(
     [dash.dependencies.Output('gsod-map', 'figure'),
      dash.dependencies.Output('gsod-temp-plot', 'figure'),
      dash.dependencies.Output('gsod-wdsp-plot', 'figure'),
     ],
     [dash.dependencies.Input('gsod-range-slider', 'start_date'),
      dash.dependencies.Input('gsod-range-slider', 'end_date'),
      dash.dependencies.Input('gsod-station-dropdown', 'value')
     ]
)
def update_gsod(start_date, end_date, value):
    idx = list(gsod[(gsod['date'] <= end_date) & (gsod['date'] >= start_date)].index)
    gsod_subset = gsod.iloc[idx,:]
    
    gsod_subset2 = gsod[gsod['name'].isin(value)]
    
    return generate_gsod_fig(gsod_subset), generate_gsod_temp_plot(gsod_subset2), generate_gsod_wdsp_plot(gsod_subset2)



@app.callback(
    dash.dependencies.Output('image', 'src'),
    [dash.dependencies.Input('image-dropdown', 'value')]
)
def update_image_src(value):
    image_path = static_image_route + 'plot_' + value + '.png'
    image_base64=base64.b64encode(open(image_path, 'rb').read()).decode('ascii') 
    #print(image_path)
    return 'data:image/png;base64,{}'.format(image_base64)


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/page-0':
        return page_0_layout
    elif pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    else:
        #pass
        return page_0_layout


if __name__ == '__main__':
    app.run_server(debug=True)
