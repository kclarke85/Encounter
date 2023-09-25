import pandas as pd
import holoviews as hv
import geoviews as gv
import panel as pn

# Sample data for the bubble chart
bubble_data = pd.DataFrame({
    'X': [1, 2, 3, 4, 5],
    'Y': [10, 11, 12, 13, 14],
    'Size': [100, 200, 300, 400, 500],
    'Label': ['A', 'B', 'C', 'D', 'E']
})

# Sample data for the table chart
table_data = pd.DataFrame({
    'Name': ['John', 'Alice', 'Bob', 'Eve', 'Mike'],
    'Age': [28, 24, 22, 25, 30],
    'City': ['New York', 'Los Angeles', 'Chicago', 'San Francisco', 'Boston']
})

# Create a Bubble Chart using HoloViews
bubble_chart = hv.Scatter(bubble_data, kdims=['X', 'Y'], vdims=['Size', 'Label'])

# Create a Table Chart using HoloViews
table_chart = hv.Table(table_data)

# Create a Geolocation Chart for Atlanta, GA using GeoViews
atlanta_location = gv.Points([(-84.387982, 33.748995)]).opts(size=10, color='red')
geo_chart = gv.tile_sources.Wikipedia * atlanta_location

# Create a Panel Dashboard to arrange the charts
dashboard = pn.Row(
    pn.Column('## Bubble Chart', bubble_chart),
    pn.Column('## Table Chart', table_chart),
    pn.Column('## Atlanta, GA Geolocation', geo_chart),
)

# Display the dashboard
dashboard.servable()
