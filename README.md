# Heatwave Dashboard

## Project Overview
The **Heatwave Dashboard** is an interactive web application developed with Dash and Plotly, designed to visualize heatwave anomalies globally. This application allows users to:

- Select a specific year and projection type to view heatwave anomalies.
- Explore temperature changes over a range of years with an average line graph.
- Filter and display data for selected countries within specific year ranges.
- Visualize heatwave patterns using choropleth maps with geojson data.

The dashboard leverages global heatwave data from a CSV file and presents it in an intuitive, interactive way for easier analysis.

## Features
- **Year Selection**: Choose the year to visualize heatwave data.
- **Projection Type**: Select from various map projection types (e.g., Equirectangular, Mercator, Orthographic).
- **Line Graphs**: Display temperature changes over a selected range of years.
- **Country Filter**: Filter and view data for specific countries, with customizable year ranges.
- **Choropleth Map**: Interactive map showing temperature changes globally or for selected countries.

## Technologies Used
- **Dash**: Framework for building interactive web applications.
- **Plotly**: For data visualization, including choropleth maps and line graphs.
- **Pandas**: For data manipulation and processing.
- **GeoJSON**: For world map data.

## Dataset
[Heatwave Excessive Heat Anomalies By Year](https://www.kaggle.com/datasets/muhammadroshaanriaz/heatwave-excessive-heat-anomalies-by-year)
