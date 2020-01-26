import dash
import dash_core_components as dcc
import dash_html_components as html
from datetime import datetime as dt

import numpy as np
import pandas as pd
import plotly.graph_objs as go
import pandas as pd
import geopandas as gpd



data = gpd.read_file("data/wildfire_map_data.shp")
data['ACQ_DATE'] = pd.to_datetime(data['ACQ_DATE'])


gsod = gpd.read_file("data/aus_gsod_records_small.shp")


stn_names = np.array(gsod['name'].value_counts().index).tolist()
dropdown_options = [*map(lambda t:{'label':t, 'value': t}, stn_names)]
#gsod = pd.read_csv("data/aus_gsod_records_small.csv")
gsod_s = gsod[gsod['date']=='2020-01-14']


gsod['date'] = pd.to_datetime(gsod['date'])




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
            colorbar_title='Mean wind speed (knots)'
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


gsod_fig = go.Figure(data=go.Scattergeo(
        lon=gsod_s['geometry'].x,
        lat=gsod_s['geometry'].y,
        mode='markers',
        text=gsod_s['text'],
        marker=dict(
            size=gsod_s['wdsp'].map(lambda t:np.sqrt(t).round()+1),
            opacity=0.8,
            reversescale=True, autocolorscale=False,
            line=dict(width=0),
            colorscale='Inferno',
            cmin=gsod_s['temp'].min(),
            cmax=gsod_s['temp'].max(),
            #cmax=test['FRP'].max(),
            color=gsod_s['temp'],
            colorbar_title='Mean wind speed (knots)'
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
#html.P("The devastating wildfire in Australia has brought huge destruction to the country")

app = dash.Dash(__name__)
app.layout = html.Div(
    style={'backgroundColor': 'white'},
    children = [
        
        html.Div([
            
            html.H2('Australian wildfire distribution'),
            
            html.H3(
                children='Select date range',
                style={
                    'textAlign': 'left',
                    'color': 'black'
                }
            ),
            dcc.DatePickerRange(
                id="wildfire-date-range-slider",
                month_format='MMM Do, YY',
                start_date=dt(2018,1,1),
                end_date=dt(2020,1,16)
            ),
            html.H3(
                children='Select sensor',
                style={
                    'textAlign': 'left',
                    'color': 'black'
                }
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
            html.H3(
                children='Filter wildfire by FRP',
                style={
                    'textAlign': 'left',
                    'color': 'black'
                }
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
            html.H2('Ground surface summary of the day'),
            html.H3(
                children='Select date range',
                style={
                    'textAlign': 'left',
                    'color': 'black'
                }
            ),
            dcc.DatePickerRange(
                id="gsod-range-slider",
                month_format='MMM Do, YY',
                start_date=dt(2019,12,16),
                end_date=dt(2020,1,16)
            ),
            
            
            html.Div([
                dcc.Graph(
                id="gsod-map",
                figure=gsod_fig
                )
            ]),
            html.Div(id='test')
        ],style={'backgroundColor':'AliceBlue', 'width':'49%', 'float':'right'})    
    ]
)


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



'''

@app.callback(
    dash.dependencies.Output('test', 'children'),
    #dash.dependencies.Output('wildfire-map', 'figure'),
    []
)
def update_output(value):
    data_subset = data[data['INSTRUMENT'].isin(value)]
    return generate_wildfire_fig(data_subset)
'''


if __name__ == '__main__':
    app.run_server(debug=True)



'''
            html.H3(
                children='Filter station',
                style={
                    'textAlign': 'left',
                    'color': 'black'
                }
            ),
            dcc.Dropdown(
                id="gsod_stn_dropdown",
                options=dropdown_options,
                value=['MELBOURNE INTL', 'CAPE BORDA AWS','NEPTUNE ISLAND'],
                multi=True
            ),
'''