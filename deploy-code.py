import pandas as pd
import requests

df = pd.read_csv('Data/HeatwaveAnomalies.csv', delimiter=';')
df

for i in range(2023, 1999, -1):
    df[f'January {i}'] = df[f'January {i}'].str.replace(',', '.').astype(float)

for i in range(2023, 1999, -1):
    df[f'December {i}'] = df[f'December {i}'].str.replace(',', '.').astype(float)

df

geojson_url = 'https://raw.githubusercontent.com/johan/world.geo.json/master/countries.geo.json'
geojson = requests.get(geojson_url).json()
geojson_countries = [country['properties']['name'] for country in geojson['features']]

not_in_geojson = df[~df['Country'].isin(geojson_countries)]['Country'].unique()
print(not_in_geojson)

df = df[df['Country'].isin(geojson_countries) | (df['Country'] == 'World')]
df

import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objs as go

external_stylesheets = ['style.css']

app = dash.Dash(external_stylesheets=external_stylesheets)

countries = df['Country'].unique()
countries = [country for country in countries if country != 'World']

country_options = [{'label': country, 'value': country} for country in countries]

year_options = [{'label': f"{month} {year}", 'value': f"{month} {year}"}
                for year in range(2023, 1999, -1)
                for month in ['January', 'December']]

default_start_year = 'Absolute Change 2000'
default_end_year = 'Absolute Change 2023'

year_options_graph_start = [{'label': f"{year}", 'value': f"Absolute Change {year}"}
                            for year in range(2023, 1999, -1)]

year_options_graph_end = [{'label': f"{year}", 'value': f"Absolute Change {year}"}
                          for year in range(2023, 1999, -1)]

default_start_year_selected = 'Absolute Change 2000'
default_end_year_selected = 'Absolute Change 2023'

year_options_graph_start_selected = [{'label': f"{year}", 'value': f"Absolute Change {year}"}
                            for year in range(2023, 1999, -1)]

year_options_graph_end_selected = [{'label': f"{year}", 'value': f"Absolute Change {year}"}
                          for year in range(2023, 1999, -1)]

projection_options = [
    {'label': 'Equirectangular', 'value': 'equirectangular'},
    {'label': 'Mercator', 'value': 'mercator'},
    {'label': 'Orthographic', 'value': 'orthographic'},
    {'label': 'Natural Earth', 'value': 'natural earth'},
    {'label': 'Kavrayskiy7', 'value': 'kavrayskiy7'},
    {'label': 'Miller', 'value': 'miller'},
    {'label': 'Robinson', 'value': 'robinson'},
    {'label': 'Mollweide', 'value': 'mollweide'},
    {'label': 'Sinusoidal', 'value': 'sinusoidal'},
]

app.title = 'Heatwave Dashboard'

app.layout = html.Div([
    html.Div([
        html.Div([
            html.Div('Heatwave Anomalies Of The World', className='title'),
            html.Div([
                html.Div('World Heatwave', className='sub-title'),
                html.Div([
                    html.Div('Select Year', className='input-label'),
                    dcc.Dropdown(
                        className='dropdown-input',
                        id='year-dropdown',
                        options=year_options,
                        value='December 2023'
                    ),
                    html.Div('Projection Type', className='input-label'),
                    dcc.Dropdown(
                        id='projection-dropdown',
                        options=projection_options,
                        value='equirectangular',
                        clearable=False,
                    ),
                ], className='input-container'),
            ], className='sidebar-section'),

            html.Div([
                html.Div('World Line Graph', className='sub-title'),
                html.Div([
                    html.Div('Year Range', className='input-label'),
                    html.Div([
                        dcc.Dropdown(
                            className='dropdown-input',
                            id='year-dropdown-graph-start',
                            options=year_options_graph_start,
                            value=default_start_year  # Default start year
                        ),
                        html.Div('to', className='hyphen'),
                        dcc.Dropdown(
                            className='dropdown-input',
                            id='year-dropdown-graph-end',
                            options=year_options_graph_end,
                            value=default_end_year  # Default end year
                        ),
                    ], className='year-container'),
                ], className='input-container'),
            ], className='sidebar-section'),

            html.Div([
                html.Div('Selected Countries', className='sub-title'),
                html.Div([
                    html.Div('Select Countries', className='input-label'),
                    dcc.Dropdown(
                        className='dropdown-input',
                        id='country-dropdown',
                        options=country_options,
                        value=[],
                        multi=True
                    ),
                    html.Div('Year Range', className='input-label'),
                    html.Div([
                        dcc.Dropdown(
                            className='dropdown-input',
                            id='year-dropdown-selected-countries-start',
                            options=year_options_graph_start_selected,
                            value=default_start_year_selected
                        ),
                        html.Div('to', className='hyphen'),
                        dcc.Dropdown(
                            className='dropdown-input',
                            id='year-dropdown-selected-countries-end',
                            options=year_options_graph_end_selected,
                            value=default_end_year_selected
                        ),
                    ], className='year-container'),
                ], className='input-container'),
            ], className='sidebar-section'),
        ], className='sidebar-container')
    ], className='sidebar'),

    html.Div([
        html.Div([
            html.Div(id='map-graph-title', className='graph-title'),
            dcc.Graph(
                id='choropleth-map',
                className='dccGraph',
                config={'responsive': True}
            ),
        ], className='map-graph-container'),
        html.Div([
            html.Div([
                html.Div(id='line-graph-title', className='graph-title'),
                dcc.Graph(id='line-graph', className='dccGraph'),
            ], className='line-graph'),
            html.Div([
                html.Div(id='line-graph-selected-countries-title', className='graph-title'),
                dcc.Graph(id='line-graph-selected-countries', className='dccGraph'),
            ], className='line-graph'),
        ], className='line-graph-container'),
    ], className='content-section'),

], className='container')

@app.callback(
    Output('map-graph-title', 'children'),
    [
        Input('year-dropdown', 'value'),
    ]
)
def update_map_graph_title(year):
    return f'Heatwave Anomalies Of The World - {year}'

@app.callback(
    Output('line-graph-title', 'children'),
    [
        Input('year-dropdown-graph-start', 'value'),
        Input('year-dropdown-graph-end', 'value'),
    ]
)
def update_line_graph_title(start_year_col, end_year_col):
    start_year = int(start_year_col.split()[2])
    end_year = int(end_year_col.split()[2])
    return f'Heatwave Temperature Change for World {start_year} to {end_year}'

@app.callback(
    Output('line-graph-selected-countries-title', 'children'),
    [
        Input('year-dropdown-selected-countries-start', 'value'),
        Input('year-dropdown-selected-countries-end', 'value'),
    ]
)
def update_line_graph_selected_countries_title(start_year_col, end_year_col):
    start_year = int(start_year_col.split()[2])
    end_year = int(end_year_col.split()[2])
    return f'Heatwave Temperature Change for Selected Countries {start_year} to {end_year}'

@app.callback(
    Output('year-dropdown-graph-start', 'options'),
    [Input('year-dropdown-graph-end', 'value')]
)
def update_start_year_options(selected_end_year):
    end_year = int(selected_end_year.split()[2])
    
    updated_options = [{'label': f"{year}", 'value': f"Absolute Change {year}"}
                       for year in range(2000, end_year)]
    
    return updated_options

@app.callback(
    Output('year-dropdown-graph-end', 'options'),
    [Input('year-dropdown-graph-start', 'value')]
)
def update_end_year_options(selected_start_year):
    start_year = int(selected_start_year.split()[2])
    
    updated_options = [{'label': f"{year}", 'value': f"Absolute Change {year}"}
                       for year in range(start_year + 1, 2024)]
    
    return updated_options

@app.callback(
    Output('year-dropdown-selected-countries-start', 'options'),
    [Input('year-dropdown-selected-countries-end', 'value')]
)
def update_start_year_options_selected(selected_end_year):
    end_year = int(selected_end_year.split()[2])
    
    updated_options = [{'label': f"{year}", 'value': f"Absolute Change {year}"}
                       for year in range(2000, end_year)]
    
    return updated_options

@app.callback(
    Output('year-dropdown-selected-countries-end', 'options'),
    [Input('year-dropdown-selected-countries-start', 'value')]
)
def update_end_year_options_selected(selected_start_year):
    start_year = int(selected_start_year.split()[2])
    
    updated_options = [{'label': f"{year}", 'value': f"Absolute Change {year}"}
                       for year in range(start_year + 1, 2024)]
    
    return updated_options

@app.callback(
    Output('choropleth-map', 'figure'),
    [
        Input('year-dropdown', 'value'),
        Input('country-dropdown', 'value'),
        Input('projection-dropdown', 'value')
    ]
)
def update_choropleth_map(selected_year, selected_countries, projection_type):
    if not selected_countries:
        data_country = df[['Country', selected_year]]
    else:
        data_countries = df[df['Country'].isin(selected_countries)]
        data_country = data_countries[['Country', selected_year]]
    
    data_country.columns = ['Country', 'Value']

    fig = px.choropleth(data_country,
                        locations='Country',
                        locationmode='country names',
                        color='Value',
                        hover_name='Country',
                        color_continuous_scale=px.colors.sequential.Blues,
                        labels={'Value': 'Temperature Change'})
    
    fig.update_layout(
        geo=dict(
            showframe=False,
            showcoastlines=True,
            projection_type=projection_type,
        ),
        autosize=True,
        margin=dict(l=10, r=10, t=30, b=10),
        font=dict(family='Maison Neue Extended', size=12, color='Black', weight='bold'),
    )

    return fig

@app.callback(
    Output('line-graph', 'figure'),
    [
        Input('year-dropdown-graph-start', 'value'),
        Input('year-dropdown-graph-end', 'value'),
    ]
)
def update_line_graph(start_year_col, end_year_col):
    start_year = int(start_year_col.split()[2])
    end_year = int(end_year_col.split()[2])

    years = [year for year in range(start_year, end_year + 1)]
    years_col = [f'Absolute Change {year}' for year in years]

    data_world = df.loc[df['Country'] == 'World', years_col].squeeze()

    x_data = [f'{year}' for year in years]
    y_data = data_world.values.astype(float)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_data, y=y_data, mode='lines', name='World'))
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Temperature Change',
        showlegend=True,
        xaxis=dict(
            autorange=True,
            showgrid=True, 
            gridwidth=1, 
            gridcolor='lightgray', 
            zeroline=False
        ),
        yaxis=dict(
            autorange=True,
            scaleanchor="x",
            scaleratio=1,
            showgrid=True, 
            gridwidth=1, 
            gridcolor='lightgray', 
            zeroline=False
        ),
        autosize=True,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family='Maison Neue Extended', size=12, color='Black', weight='bold'),
    )

    return fig

@app.callback(
    Output('line-graph-selected-countries', 'figure'),
    [
        Input('year-dropdown-selected-countries-start', 'value'),
        Input('year-dropdown-selected-countries-end', 'value'),
        Input('country-dropdown', 'value')
    ]
)
def update_line_graph_selected_countries(start_year_col, end_year_col, selected_countries):
    start_year = int(start_year_col.split()[2])
    end_year = int(end_year_col.split()[2])

    years = [year for year in range(start_year, end_year + 1)]
    years_col = [f'Absolute Change {year}' for year in years]

    data_countries = df[df['Country'].isin(selected_countries)][['Country'] + years_col]

    fig = go.Figure()
    for country in selected_countries:
        country_data = data_countries[data_countries['Country'] == country]
        y_data = country_data.values.tolist()[0][1:]
        fig.add_trace(go.Scatter(x=years, y=y_data, mode='lines', name=country))
    
    fig.update_layout(
        xaxis_title='Year',
        yaxis_title='Temperature Change',
        showlegend=True,
        xaxis=dict(
            autorange=True,
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            zeroline=False
        ),
        yaxis=dict(
            autorange=True,
            scaleanchor="x",
            scaleratio=1,
            showgrid=True,
            gridwidth=1,
            gridcolor='lightgray',
            zeroline=False
        ),
        autosize=False,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor='white',
        plot_bgcolor='white',
        font=dict(family='Maison Neue Extended', size=12, color='Black', weight='bold'),
        )
    
    return fig

app.run_server(debug=False)