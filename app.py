import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px
from dash.dependencies import Input, Output

gentr = pd.read_csv('data/gentrification.csv')
mapbox_access_token = 'pk.eyJ1IjoiZ3VqaW1sIiwiYSI6ImNrY21pamg4dDAxZmEyc2xjdzZtNjY3YTIifQ.PKI5m9ZE6OTgj_ZhBCHyiw'

# Initialize the app
app = dash.Dash(__name__)
app.config.suppress_callback_exceptions = True

building_sales = pd.read_csv('data/sales.csv')
building_sales = building_sales[building_sales['SALE PRICE'] != 0]
building_sales['SALE DATE'] = pd.to_datetime(building_sales['SALE DATE'])
time_price = building_sales[['SALE DATE','SALE PRICE']]
df_time = time_price.set_index(['SALE DATE'])
time_price_means = df_time.resample('M').mean()
time_price_means['Date'] = time_price_means.index
fig1 = px.line(time_price_means, x='Date', y='SALE PRICE')
fig1['layout'].update({'height': 200})


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
                                 dcc.Graph(id='graph1', figure=fig1),
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
    fig = go.Figure(go.Scattermapbox(lat=filtered_gentr['Lat'],lon=filtered_gentr['Lon'],mode='markers',marker=go.scattermapbox.Marker(color=filtered_gentr['gentrifica'])))
    fig.update_layout(mapbox=dict(accesstoken=mapbox_access_token, center=dict(lon=-73.99,lat=40.72), zoom=10))
    fig.update_layout(margin={"r":20,"t":20,"l":20,"b":20})
    fig.update_layout({'height': 200, 'width': 800})
    fig.update_layout(transition_duration=500)
    return fig



if __name__ == '__main__':
    app.run_server(debug=False)
