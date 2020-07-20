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
import datetime as dt
from datetime import datetime, timedelta
import numpy as np

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
app.title = 'Displacement visualization tool'
server = app.server


### STYLES
LeftText = {'margin-left':'25px','margin-right':'25px', 'color':'whitesmoke', 'font-size':'12px', 'text-align': 'justify', 'text-justify': 'inter-word'}
LeftTextY = {'margin-left':'15px','margin-right':'25px', 'color':'purple', 'font-size':'14px', 'text-align': 'justify', 'text-justify': 'inter-word', 'font-weight' :'bold'}
LeftTextSmall = {'margin-left':'15px','margin-right':'25px', 'color':'purple', 'font-size':'10px', 'text-align': 'justify', 'text-justify': 'inter-word'}
CenterText = {'color':'whitesmoke', 'font-size':'12px'}
CenterTextLink = {'color':'rgb(253, 255, 136)', 'font-size':'12px'}
LeftTitle = {'color':'whitesmoke','text-decoration': 'underline'}


### DOWNLOADS
pred_df_rh = pd.read_csv('data/rent_predictions_rh.csv')
pred_df_ny = pd.read_csv('data/rent_predictions_ny.csv')
gentrification_2018_df = pd.read_csv('data/gentrification_2018_df.csv')
gentrification_2018_ny = pd.read_csv('data/ny_gentrification_2018.csv')
evictions_df = pd.read_csv('data/ny_evictions.csv')
redhook_5yr_prediction = pd.read_csv('data/redhook_5_gentrification_prediction.csv')
redhook_10yr_prediction = pd.read_csv('data/redhook_10_gentrification_prediction.csv')


## OPEN GEOJSON
with open('data/redhook_clipped_gp_2018.geojson') as response:
    tracts = json.load(response)
with open('data/ny_clipped_gp_2018.geojson') as response:
    ny_map = json.load(response)
with open('data/ny_zip.geojson') as response:
    ny_zip = json.load(response)

## FURTHER CHARTS
ny_trace = go.Scatter(
    name='New York',
    x=pred_df_ny['date'],
    y=pred_df_ny['median_rent_all'],
    mode='lines',
    line=dict(color='rgb(31, 119, 180)'),
    fillcolor='rgba(68, 68, 68, 0.3)') 

rh_trace = go.Scatter(
    name='Red Hook',
    x=pred_df_rh['date'],
    y=pred_df_rh['median_rent_all'],
    mode='lines',
    line=dict(color='rgb(205,92,92)'),
    fillcolor='rgba(68, 68, 68, 0.3)')

data = [ny_trace, rh_trace]

layout = go.Layout(
    xaxis=dict(title='Year'),
    yaxis=dict(title='Median Rent USD'),
    title='Median Rent Predictions 5 and 10 Yrs',
    showlegend = True)

fig_further1 = go.Figure(data=data, layout=layout)
fig_further1.update_layout(shapes=[
    dict(
      type= 'line',
      yref= 'paper', y0= 0, y1= 1,
      xref= 'x', x0= datetime(year=2020,month=5, day=31), x1= datetime(year=2020,month=5, day=31)
    )
])
fig_further1.update_layout({'height': 350, 'width': 1005})

## APPLICATION START

## LAYOUT DESIGN
app.layout = html.Div(className="row",
    children=[
        html.Div(className='column left',
            children=[
                html.Br(),
                html.Img(src='assets/NYUCUSP.png'),
                html.Br(),
                html.Br(),
                html.Div(className='dropdown_neighboors',style={'background-color': 'whitesmoke'},
                    children=[
                        html.Br(),
                        html.P('Select the type of visualization:', style=LeftTextY),
                        dcc.Dropdown(id='map-selector', options=[
                            {'label': 'Gentrification for Red Hook - Current Year', 'value': 'GRH_CY'},
                            {'label': 'Gentrification for NY - Current Year', 'value': 'GNY_CY'},
                            {'label': 'Residential Evictions for NY - Current Year', 'value': 'RENY_CY'},
                            {'label': 'Commercial Evictions for NY - Current Year', 'value': 'CENY_CY'},
                            {'label': 'Gentrification Prediction  for Red Hook - 5 Years', 'value': 'GPRH_5Y'},
                            {'label': 'Gentrification Prediction  for Red Hook - 10 Years', 'value': 'GPRH_10Y'}
                        ],multi=False, value="GNY_CY", style={'font-size': '12px','backgroundColor': '#27272710'} ),
                        html.P('( HOW TO USE: Select one of the 6 visualizations available for the area of NYC in the dropdown box bellow. In a few seconds the main visualization map will update. You can use the mouse to navigate in the map )', style=LeftTextSmall),
                        html.Br()
                ]),
                html.Br(),
                html.H5('ABOUT THIS TOOL', style=LeftTitle),
                html.P('This website is the visualization part of the Digital CEQR capstone project group, NYU CUSP class of 2020.', style=LeftText),
                html.P('The purpose of this tool is to visualize the results derived from the analysis performed by the team in collaboration with the sponsor of this project (inCitu).', style=LeftText),
                html.Br(),
                html.Br(),
                html.A('[ GO BACK TO THE PROJECT MAIN SITE ]', href='https://ericzhuang0.wixsite.com/website-1', style=CenterTextLink),
                html.Br(),
                html.Br(),
                html.Div(className='NYUBOX',style={'background-color': '#57068c','text-align': 'center'},
                    children=[
                html.P('NYU CUSP - 2020', style=CenterText)])                
            ]),
        html.Div(className='column right',
            children=[dcc.Graph(id='displacement_map')]),
        html.Div(className='column right', style={'background-color': 'whitesmoke'},
            children=[html.H2('Scroll down for result analysis...'),
                    dcc.Graph(id='FurtherGraph1', figure=fig_further1),
                    html.H2('Final results for Red Hook Area:'),
                    html.P('Safe for approving rezoning proposals in Redhook? - “Safe”'),
                    html.P('Probability of Gentrification in Redhook in 5 Years - “Low”'),
                    html.P('Risk of Residential Eviction in Redhook - “Low”'),
                    html.P('Risk of Commercial Eviction in Redhook - “Medium”'),
                    html.P('Commercial Evictions in Redhook experienced mostly by small businesses like Tobacco Retailers '),
                    html.P('Redhook Property Price Percentage Increase (5 Yrs Prediction) - 18%'),
                    html.P('Redhook Property Price Percentage Increase (10 Yrs Prediction) - 24%')
            ])
    ])


## CALLBACKS (to update the charts)
@app.callback(
    Output('displacement_map', 'figure'),
    [Input('map-selector', 'value')])
def update_figure(selected_map):
    typeofmap = gentrification_2018_ny
    geojsonobject = ny_map
    fidkey = 'properties.geo_id'
    clr = 'prediction'
    lctions = 'geo_id'
    rngclrmin, rngclrmax = 0, 1
    lbls = 'Gentrification Prediction - NY'

    if selected_map == 'GNY_CY':
        typeofmap = gentrification_2018_ny
        geojsonobject = ny_map
        fidkey = 'properties.geo_id'
        clr = 'prediction'
        lctions = 'geo_id'
        rngclrmin, rngclrmax = 0, 1
        lbls = 'Gentrification Prediction - NY'
        lat,lon,zoo = 40.71, -74, 9
    elif selected_map == 'GRH_CY':
        typeofmap = gentrification_2018_df
        geojsonobject = tracts
        fidkey = 'properties.geo_id'
        clr = 'prediction'
        lctions = 'geo_id'
        rngclrmin, rngclrmax = 0, 0.1
        lbls = 'Gentrification Prediction - RedHook'
        lat,lon,zoo = 40.67, -74, 12
    elif selected_map == 'RENY_CY':
        typeofmap = evictions_df 
        geojsonobject = ny_zip
        fidkey = 'properties.MODZCTA'
        clr = 'residential_pctl_score'
        lctions = 'MODZCTA'
        rngclrmin, rngclrmax = 0, 100
        lbls = 'Residential Evictions Percentile Score'
        lat,lon,zoo = 40.71, -74, 9
    elif selected_map == 'CENY_CY':
        typeofmap = evictions_df 
        geojsonobject = ny_zip
        fidkey = 'properties.MODZCTA'
        clr = 'commercial_pctl_score'
        lctions = 'MODZCTA'
        rngclrmin, rngclrmax = 0, 100
        lbls = 'Commercial Evictions Percentile Score'
        lat,lon,zoo = 40.71, -74, 9
    elif selected_map == 'GPRH_5Y':
        typeofmap = redhook_5yr_prediction 
        geojsonobject = tracts
        fidkey = 'properties.geo_id'
        clr = 'prediction'
        lctions = 'geo_id'
        rngclrmin, rngclrmax = 0, 0.1
        lbls = 'Gentrification Prediction 5 Yrs - RedHook'
        lat,lon,zoo = 40.67, -74, 12
    elif selected_map == 'GPRH_10Y':
        typeofmap = redhook_10yr_prediction 
        geojsonobject = tracts
        fidkey = 'properties.geo_id'
        clr = 'prediction'
        lctions = 'geo_id'
        rngclrmin, rngclrmax = 0, 0.1
        lbls = 'Gentrification Prediction 10 Yrs - RedHook'
        lat,lon,zoo = 40.67, -74, 12


    
    plotmap = px.choropleth_mapbox(typeofmap, geojson=geojsonobject,locations = lctions, featureidkey=fidkey, color=clr, color_continuous_scale="RdBu_r", range_color=(rngclrmin, rngclrmax), mapbox_style="carto-positron", zoom=zoo, center = {"lat": lat, "lon": lon}, opacity=0.55, labels={'prediction':'Pred'})
    plotmap.update_layout(margin={"r":0,"t":0,"l":0,"b":10})
    plotmap.update_layout({'height': 500, 'width': 1000})
    return plotmap

if __name__ == '__main__':
    app.run_server(debug=False)
