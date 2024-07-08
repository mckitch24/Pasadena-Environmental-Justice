
# general libaries 
import pandas as pd
import geopandas as gpd
import plotly.express as px
import os
import censusgeocode as cg
import plotly.graph_objects as go


# Dash App specific libraries 
from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output
# from functions import address_to_tract  # Importing the function from geocoding.py
from dash.exceptions import PreventUpdate


# function
def address_to_tract(address):
    result = cg.address(address, city='Pasadena', state='CA', returntype = 'geographies')
    tract = result[0]['geographies']['Census Tracts'][0]['GEOID']
    return tract

# Data set-up

# CalEnviroScreen
california_EJ = pd.read_excel('data/calenviroscreen40resultsdatadictionary_F_2021.xlsx')
pasadena_EJ = california_EJ[california_EJ['Approximate Location'].str.contains('Pasadena', na=False)]

# Census Tract Shaefiles
tracts = gpd.read_file('data/cb_2018_06_tract_500k')
tracts['GEOID'] = tracts['GEOID'].astype('int64') # to allow a merge

# Merge
data = tracts.merge(pasadena_EJ, left_on='GEOID', right_on='Census Tract')


# Create an instance of the dash class

app = Dash(__name__)

app.layout = html.Div([
    html.H4('Pasadena Environmental Justice Communities'),

    html.Div(children='''
        A visualization of environmental and socioeconomic CalEnviroScreen metrics
    '''),

    html.Div([
        html.Div([

            # metric choice
            
            html.H4('Select a metric'),
            html.Div(
                dcc.Dropdown(
                    id='metric',
                    options=[
                        {'label': 'CalEnviroScreen Score', 'value': 'CES 4.0 Percentile'},
                        {'label': 'Pollution Burden', 'value': 'Pollution Burden Pctl'},
                        {'label': 'Population Characteristics', 'value': 'Pop. Char. Pctl'}
                    ],
                    value='CES 4.0 Percentile',
                    style={'width': '300px'}  
                ),
                style={'margin-bottom': '20px'}  # Add margin to space out elements
            ),

            # find location
            html.H4('Find your census tract'),
            html.Div(
                dcc.Input(
                    id="address",
                    value="",
                    className="w-100",
                    placeholder="street address",
                    style={'width': '300px'},
                ),
                style={'margin-bottom': '20px'}  # Add margin to space out elements
            ),
            html.Div(id='tract-output', style={'margin-top': '20px'})
            ], style={'display': 'inline-block', 'verticalAlign': 'top', 'margin-right': 'auto', 'margin-left': 'auto','width': '30%'}),
                
        # graph display
        html.Div([
            dcc.Graph(id="graph")
        ], style={'display': 'inline-block', 'verticalAlign': 'top','margin-left': 'auto', 'margin-right': 'auto','width': '70%'})
    ], style={'display': 'flex', 'alignItems': 'flex-start','width': '100%'})
], style={
    'textAlign': 'center',
    "margin-left": "3%",
    "margin-right": "3%"}
)



@app.callback(
    Output("tract-output", "children"),
    Output("graph", "figure"),
    Input('address', 'value'),
    Input("metric",'value'))

def display_choropleth(address, metric):

    if address:
        try:
            tract = address_to_tract(address)
            tract_output = f'Tract number {tract}'
        except Exception:
            raise PreventUpdate
    else:
        tract_output = ''
        tract = None

    # general code for map

    # static and no streets
    # fig = px.choropleth(data,
    #                     geojson=data.geometry,
    #                     locations=data.index,
    #                     color=metric,  # where the plot changes via input
    #                     hover_name="Census Tract",
    #                     hover_data=["CES 4.0 Percentile"],
    #                     projection="mercator",
    #                     color_continuous_scale='RdYlGn',
    #                     range_color=(0, 100)) 
    # fig.update_geos(fitbounds="locations", visible=False)

    # dynamic and with streets
    fig = px.choropleth_mapbox(data,
                        geojson=data.geometry,
                        locations=data.index,
                        color=metric,  # where the plot changes via input
                        hover_name="Census Tract",
                        hover_data=["CES 4.0 Percentile"],
                        center = {"lat": 34.154251, "lon": -118.138472},
                        color_continuous_scale='RdYlGn',
                        zoom = 10,
                        
                        range_color=(0, 100))        
    fig.update_traces(marker_opacity=0.6)

    # highlight the address tract
    if tract is not None:
        tract_data = data[data['GEOID'] == int(tract)]
        if not tract_data.empty:
            fig.add_trace(
                # go.Choropleth(
                go.Choroplethmapbox(
                    geojson=tract_data.geometry.__geo_interface__,
                    locations=tract_data.index,
                    z=[1] * len(tract_data),
                    showscale=False,
                    marker=dict(line=dict(width=2, color='white')),
                    name='Selected Tract'
                )
            )

    fig.update_layout(mapbox_style="carto-positron")
    

    fig.update_layout(coloraxis_colorbar_x=1.2)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return tract_output, fig

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run_server(debug=True, host='0.0.0.0', port=port)