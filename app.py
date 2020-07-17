import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output
import json
from urllib.request import urlopen

gentr = pd.read_csv('data/gentrification.csv')
mapbox_access_token = 'pk.eyJ1IjoiZ3VqaW1sIiwiYSI6ImNrY21pamg4dDAxZmEyc2xjdzZtNjY3YTIifQ.PKI5m9ZE6OTgj_ZhBCHyiw'

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
server = app.server

time_price_means = pd.read_csv('data/timepricemeans.csv')
fig1 = px.line(time_price_means, x='Date', y='SALE PRICE')
fig1['layout'].update({'height': 200})



with urlopen('https://gist.githubusercontent.com/akash-y/eec842afd41ca3090ee402a235faeb37/raw/1e93801cd084e00c4b49a90582e7578689787354/test.geojson') as response:
    tracts = json.load(response)
with urlopen('https://gist.githubusercontent.com/akash-y/981a07f9924b2aec750ef05d8f0ded59/raw/c5cc1bbdd2a0a63b5ca1d70eaed3daef0cab623f/ny_gentrification_2018.geojson') as response:
    ny_map = json.load(response)
with urlopen('https://gist.githubusercontent.com/akash-y/6aa5d1fe4bfecda6b2ba7bd4b918e209/raw/04134738f6cce463f787f8a20dc2a1639e15f64c/ny_zip.geojson') as response:
    ny_zip = json.load(response)

    
gentrification_2018_df = pd.read_csv('https://gist.githubusercontent.com/akash-y/aa7e340b02ac6f8cc78b3f5698bb95b8/raw/87deac83e18a099ac02ca215e3af354c7581f4eb/redhook_predictions_2018.csv')
gentrification_2018_ny = pd.read_csv('https://gist.githubusercontent.com/akash-y/0e6a14fa614aabb16b5b35a5273e44ca/raw/ee7aace5cf795aa005cc563c02be97552633b7da/ny_gentrification_2018.csv')
evictions_df = pd.read_csv('https://gist.githubusercontent.com/akash-y/e0ffea12dde217ec49546ffa66461ce5/raw/143edbf60b34e34139545cba079124ed01833652/ny_evictions.csv')


def get_options(df_menu):
    dict_list = []
    for i, j in df_menu.iterrows(): 
        dict_list.append({'label': j[1], 'value': j[0]})
    return dict_list


app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('CEQR TOOL'),
                                 html.P('Select a neighborhood.'),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='year-slider', options=get_options(gentr[['ntacode','ntaname']].drop_duplicates()),
                                                      multi=False, 
                                                      value="BK33",
                                                      style={'backgroundColor': '#1E1E1E'}
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='graph-with-slider'),
				 dcc.Graph(id='graph1', figure=fig1)
                              ])
                              ])
        ]
)



@app.callback(
    Output('graph-with-slider', 'figure'),
    [Input('year-slider', 'value')])
def update_figure(selected):
    selectedval = selected
    filtered_gentr = gentr[gentr.ntacode == selected]
    commercial_evictions = px.choropleth_mapbox(evictions_df, geojson=ny_zip,locations = 'MODZCTA' ,featureidkey="properties.MODZCTA",color='commercial_pctl_score',
                           color_continuous_scale="Viridis",
                           range_color=(0, 100),
                           mapbox_style="carto-positron",
                           zoom=10, center = {"lat": 40.724576, "lon": -73.916812},
                           opacity=0.5,
                           labels={'prediction':'Commercial Evictions Percentile Score'}
                          )
    commercial_evictions.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    commercial_evictions.update_layout({'height': 200, 'width': 800})
    return commercial_evictions



if __name__ == '__main__':
    app.run_server(debug=False)
