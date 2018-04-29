# -*- coding: utf-8 -*-

"""
Choropleth example with Dash

Example using data on Limited English Proficiency in Portland.
Shapefile taken from:

https://gis-pdx.opendata.arcgis.com/datasets/a0e5ed95749d4181abfb2a7a2c98d7ef_121


Note that there is currently a bug in dash which breaks interactions after second layer change.
See https://github.com/plotly/dash/issues/223 for more info.
"""

import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import geopandas as gpd
import randomcolor

mapbox_key = None
if not mapbox_key:
    raise RuntimeError("Edit the file and specify your mapbox key!")

# Example shapefile from:
# https://gis-pdx.opendata.arcgis.com/datasets/a0e5ed95749d4181abfb2a7a2c98d7ef_121
# Portland Limited English Proficiency
lep_shp = 'data/lep/Limited_English_Proficiency.shp'
lep_df = gpd.read_file(lep_shp)

# Generate centroids for each polygon to use as marker locations
lep_df['lon_lat'] = lep_df['geometry'].apply(lambda row: row.centroid)
lep_df['LON'] = lep_df['lon_lat'].apply(lambda row: row.x)
lep_df['LAT'] = lep_df['lon_lat'].apply(lambda row: row.y)
lep_df = lep_df.drop('lon_lat', axis=1)

lon = lep_df['LON'][0]
lat = lep_df['LAT'][0]
center = [lat, lon]

# Generate stats for example
langs = [lng for lng in lep_df.columns
         if lng.istitle() and
         lng not in ['Id', 'Id2', 'Total_Pop_'] and
         'Shape' not in lng]

lep_df['NUM_LEP'] = lep_df[langs].sum(axis=1)

# Create hover info text
lep_df['HOVER'] = 'Geography: ' + lep_df.Geography + \
    '<br /> Num. LEP:' + lep_df.NUM_LEP.astype(str)

overlay_options = {
    lng.lower(): json.loads(lep_df.loc[lep_df[lng] > 0, :].to_json())
    for lng in langs
}

# Generate colors for each language
seed_val = 10  # Set a seed value to generate the same colors between runs
color_generator = randomcolor.RandomColor(seed=seed_val)
colors = color_generator.generate(count=len(langs))

# Setup overlay colors
overlay_color = {
    lng.lower(): shade
    for lng, shade in zip(langs, colors)
}

all_opt = {'label': 'All', 'value': 'all'}
opts = [{'label': lng.title(), 'value': lng.lower()} for lng in langs]
opts.append(all_opt)

map_layout = {
    'title': 'Portland LEP',
    'data': [{
        'lon': lep_df['LON'],
        'lat': lep_df['LAT'],
        'mode': 'markers',
        'marker': {
            'opacity': 0.0,
        },
        'type': 'scattermapbox',
        'name': 'Portland LEP',
        'text': lep_df['HOVER'],
        'hoverinfo': 'text',
        'showlegend': True,
    }],
    'layout': {
        'autosize': True,
        'hovermode': 'closest',
        'margin': {'l': 0, 'r': 0, 'b': 0, 't': 0},
        'mapbox': {
            'accesstoken': mapbox_key,
            'center': {
                'lat': lat,
                'lon': lon
            },
            'zoom': 8.0,
            'bearing': 0.0,
            'pitch': 0.0,
        },
    }
}

app = dash.Dash()

app.layout = html.Div([
    html.H1(children='Portland - Limited English Proficiency (Choropleth Example)'),
    dcc.Dropdown(
        id='overlay-choice',
        options=opts,
        value='all'
    ),
    html.Div([
        dcc.Graph(id='map-display'),
    ])
])


@app.callback(
    dash.dependencies.Output('map-display', 'figure'),
    [dash.dependencies.Input('overlay-choice', 'value')])
def update_map(overlay_choice):

    if overlay_choice == 'all':
        layers = []
        for overlay in overlay_options:
            if overlay == 'all':
                continue
            # End if

            layers.append({
                'name': overlay,
                'source': overlay_options[overlay],
                'sourcetype': 'geojson',
                'type': 'fill',
                'opacity': 0.3,
                'color': overlay_color[overlay]
            })
        # End for
    else:
        overlay_data = overlay_options.get(overlay_choice, None)
        if overlay_data is None:
            raise RuntimeError("Invalid overlay option")
        # End if

        layers = [{
            'name': overlay_choice,
            'source': overlay_data,
            'sourcetype': 'geojson',
            'type': 'fill',
            'opacity': 1.0,
            'color': overlay_color[overlay_choice]
        }]
    # End if

    tmp = map_layout
    tmp['layout']['mapbox']['layers'] = layers

    return tmp
# End update_map()


if __name__ == '__main__':
    app.run_server(debug=True, port=8051)
