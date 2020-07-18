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


gentr = pd.read_csv('data/gentrification.csv')
gentr.sort_values(by=['ntaname'], inplace=True)
mapbox_access_token = 'pk.eyJ1IjoiZ3VqaW1sIiwiYSI6ImNrY21pamg4dDAxZmEyc2xjdzZtNjY3YTIifQ.PKI5m9ZE6OTgj_ZhBCHyiw'

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True
server = app.server

time_price_means = pd.read_csv('data/timepricemeans.csv')
time_price_means['Date'] = pd.to_datetime(time_price_means['Date'])
time_price_means['Year'] = time_price_means['Date'].dt.year


pricepred = pd.read_csv('data/med_rent_pred_cons.csv')
pricepred['date'] = pd.to_datetime(pricepred['date'])
pricepred['Year'] = pricepred['date'].dt.year
pricepred.sort_values(by = 'date', inplace=True)

groups = pricepred.groupby(by='Type')
data = []
colors=['blue', 'green']
for group, dataframe in groups:
    dataframe = dataframe.sort_values(by=['date'])
    trace = go.Scatter(x=dataframe.date.tolist(), 
                       y=dataframe.future_price.tolist(),
                       marker=dict(color=colors[len(data)]),
                       name=group)
    data.append(trace)

layout =  go.Layout(xaxis={'title': 'Time'},
                    yaxis={'title': 'PRICE PRED'},
                    hovermode='closest')
figpred = go.Figure(data=data, layout=layout)
figpred['layout'].update({'height': 130})  
figpred.update_layout(margin={"r":20,"t":0,"l":20,"b":0})



with urlopen('https://gist.githubusercontent.com/akash-y/eec842afd41ca3090ee402a235faeb37/raw/1e93801cd084e00c4b49a90582e7578689787354/test.geojson') as response:
    tracts = json.load(response)
with urlopen('https://gist.githubusercontent.com/akash-y/981a07f9924b2aec750ef05d8f0ded59/raw/c5cc1bbdd2a0a63b5ca1d70eaed3daef0cab623f/ny_gentrification_2018.geojson') as response:
    ny_map = json.load(response)
with urlopen('https://gist.githubusercontent.com/akash-y/6aa5d1fe4bfecda6b2ba7bd4b918e209/raw/04134738f6cce463f787f8a20dc2a1639e15f64c/ny_zip.geojson') as response:
    ny_zip = json.load(response)

    
gentrification_2018_df = pd.read_csv('https://gist.githubusercontent.com/akash-y/aa7e340b02ac6f8cc78b3f5698bb95b8/raw/87deac83e18a099ac02ca215e3af354c7581f4eb/redhook_predictions_2018.csv')
gentrification_2018_ny = pd.read_csv('https://gist.githubusercontent.com/akash-y/0e6a14fa614aabb16b5b35a5273e44ca/raw/ee7aace5cf795aa005cc563c02be97552633b7da/ny_gentrification_2018.csv')
evictions_df = pd.read_csv('https://gist.githubusercontent.com/akash-y/e0ffea12dde217ec49546ffa66461ce5/raw/143edbf60b34e34139545cba079124ed01833652/ny_evictions.csv')
redhook_5yr_prediction = pd.read_csv('https://gist.githubusercontent.com/akash-y/4b3e114d2cfdd22aab9462d4db942999/raw/16ae0b48e1094d27a4e3460c3cfb4dda6f047161/redhook_5_gentrification_prediction.csv')
redhook_10yr_prediction = pd.read_csv('https://gist.githubusercontent.com/akash-y/f0a8d865efd78008f49d4f5602ffcf34/raw/1c3f7cb79e521dc3188e817610148ed044dae1b4/redhook_10_gentrification_prediction.csv')

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
                                 html.H2('CEQR TOOL', style={'font-family': 'Tahoma', 'font-size': '20px', 'color': 'yellow'}),
                                 html.Hr(),
                                 html.P('Center map in a specific neighborhood:', style={'font-family': 'Tahoma', 'font-size': '14px'}),
                                 html.Div(
                                     className='dropdown1',
                                     children=[
                                         dcc.Dropdown(id='dropdown-neighborhood', options=get_options(gentr[['ntacode','ntaname']].drop_duplicates()),
                                                      multi=False, 
                                                      value="BK33",
                                                      style={'backgroundColor': '#1E1E1E','font-family': 'Tahoma', 'font-size': '12px'}
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'}),
                                html.Br(),     
                                html.P('Select the type of map to be shown:', style={'font-family': 'Tahoma', 'font-size': '14px'}),
                                html.Div(
                                     className='dropdown2',
                                     children=[
                                         dcc.Dropdown(id='dropdown-type', options=[
                                            {'label': 'Gentrification for Red Hook - Current Year', 'value': 'GRH_CY'},
                                            {'label': 'Gentrification for NY - Current Year', 'value': 'GNY_CY'},
                                            {'label': 'Residential Evictions for NY - Current Year', 'value': 'RENY_CY'},
                                            {'label': 'Commercial Evictions for NY - Current Year', 'value': 'CENY_CY'},
                                            {'label': 'Gentrification Prediction  for Red Hook - 5 Years', 'value': 'GPRH_5Y'},
                                            {'label': 'Gentrification Prediction  for Red Hook - 10 Years', 'value': 'GPRH_10Y'}
                                        ],
                                                      multi=False, 
                                                      value="GNY_CY",
                                                      style={'backgroundColor': '#1E1E1E','font-family': 'Tahoma', 'font-size': '12px'}
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='mapplot',style={'font-family': 'Tahoma'}),
                                 html.P('Historical Sales Price', style={'font-family': 'Tahoma', 'font-size': '14px', 'color': '#949494', 'font-weight': 'bold', 'text-align': 'center'}),
                                 dcc.Graph(id='linechart'),
                                 html.P('Future Price', style={'font-family': 'Tahoma', 'font-size': '14px', 'color': '#949494', 'font-weight': 'bold', 'text-align': 'center'}),
                                 #dcc.Slider(
                                 #    id='year-slider',
                                 #    min=time_price_means['Year'].min(),
                                 #    max=time_price_means['Year'].max(),
                                 #    value=2019,
                                 #    marks={str(year): str(year) for year in time_price_means['Year'].unique()},
                                 #    step=None),
                                 dcc.Graph(id='pred', figure=figpred)
                              ])
                              ])
        ],
        style={'font-family': 'Tahoma'}
)



@app.callback(
    [Output('mapplot', 'figure'),
     Output('linechart', 'figure')],
    [Input('dropdown-neighborhood', 'value'),
     Input('dropdown-type', 'value')])
def update_map(neighborhood,typechart):
    selectedval = neighborhood
    filtered_gentr = gentr[gentr.ntacode == neighborhood]
    meanlat = filtered_gentr.loc[:,"Lat"].mean()
    meanlon = filtered_gentr.loc[:,"Lon"].mean()

    if typechart == 'GNY_CY':
        typeofmap = gentrification_2018_ny
        geojsonobject = ny_map
        fidkey = 'properties.geo_id'
        clr = 'prediction'
        lctions = 'geo_id'
        rngclrmin, rngclrmax = 0, 1
        lbls = 'Gentrification Prediction - NY'
    elif typechart == 'GRH_CY':
        typeofmap = gentrification_2018_df
        geojsonobject = tracts
        fidkey = 'properties.geo_id'
        clr = 'prediction'
        lctions = 'geo_id'
        rngclrmin, rngclrmax = 0, 0.1
        lbls = 'Gentrification Prediction - RedHook'
    elif typechart == 'RENY_CY':
        typeofmap = evictions_df 
        geojsonobject = ny_zip
        fidkey = 'properties.MODZCTA'
        clr = 'residential_pctl_score'
        lctions = 'MODZCTA'
        rngclrmin, rngclrmax = 0, 100
        lbls = 'Residential Evictions Percentile Score'
    elif typechart == 'CENY_CY':
        typeofmap = evictions_df 
        geojsonobject = ny_zip
        fidkey = 'properties.MODZCTA'
        clr = 'commercial_pctl_score'
        lctions = 'MODZCTA'
        rngclrmin, rngclrmax = 0, 100
        lbls = 'Commercial Evictions Percentile Score'
    elif typechart == 'GPRH_5Y':
        typeofmap = redhook_5yr_prediction 
        geojsonobject = tracts
        fidkey = 'properties.geo_id'
        clr = 'prediction'
        lctions = 'geo_id'
        rngclrmin, rngclrmax = 0, 0.1
        lbls = 'Gentrification Prediction 5 Yrs - RedHook'
    elif typechart == 'GPRH_10Y':
        typeofmap = redhook_10yr_prediction 
        geojsonobject = tracts
        fidkey = 'properties.geo_id'
        clr = 'prediction'
        lctions = 'geo_id'
        rngclrmin, rngclrmax = 0, 0.1
        lbls = 'Gentrification Prediction 10 Yrs - RedHook'

    plotmap = px.choropleth_mapbox(typeofmap, geojson=geojsonobject,locations = lctions, featureidkey=fidkey, color=clr,
                           color_continuous_scale="Viridis",
                           range_color=(rngclrmin, rngclrmax),
                           mapbox_style="carto-positron",
                           zoom=9, center = {"lat": meanlat, "lon": meanlon},
                           opacity=0.75,
                           labels={'prediction':'Pred'}
                          )
    plotmap.update_layout(margin={"r":20,"t":50,"l":20,"b":20})
    plotmap.update_layout({'height': 280, 'width': 760})


    #filtered_df = time_price_means[time_price_means.Year <= yearslider]
    linechart = px.line(time_price_means, x='Date', y='SALE PRICE')
    linechart['layout'].update({'height': 130, 'width': 760})
    linechart.update_layout(margin={"r":20,"t":0,"l":20,"b":0})

    return plotmap, linechart



if __name__ == '__main__':
    app.run_server(debug=True)
