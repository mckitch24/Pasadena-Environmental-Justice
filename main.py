
# general libaries 
import pandas as pd
import os
import geopandas as gpd
import plotly.express as px

# Dash App specific libraries 
from dash import Dash
from dash import dcc
from dash import html
from dash import Input, Output

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
    html.H4('Pasadena Environmental Justice'),

    html.Div(children='''
        A visualization of environmental and socioeconomic vulnerability metrics
    '''),

    html.Div([
        html.Div([
            html.H4('Select a metric'),
            dcc.RadioItems(
                id='metric',
                options=["Latitude", "Longitude"],
                value="Latitude",
                inline=False
            )

        ], style={'display': 'inline-block', 'verticalAlign': 'top', 'margin-right': '10px', 'margin-left': '100px'}),
        
        html.Div([
            dcc.Graph(id="graph")
        ], style={'display': 'inline-block', 'width': '80%', 'verticalAlign': 'top'})
    ], style={'display': 'flex', 'alignItems': 'flex-start'})
], style={
    'textAlign': 'center',
    "margin-left": "20px",
    "margin-right": "20px"}
)



@app.callback(
    Output("graph", "figure"),
    Input("metric",'value'))
def display_choropleth(metric):

    fig = px.choropleth(data,
                        geojson=data.geometry,
                        locations=data.index,
                        color=metric,  # where the plot changes via input
                        hover_name="Census Tract",
                        hover_data=["Longitude"],
                        projection="mercator")

    fig.update_geos(fitbounds="locations", visible=False)
    fig.update_layout(coloraxis_colorbar_x=0.7)
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)