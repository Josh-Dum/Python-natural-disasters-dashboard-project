import pandas as pd

natural_disaster_df = pd.read_csv('natural_disaster.csv')
df_geoloc = pd.read_csv("new_dataframe.csv")
global_temp_data = pd.read_csv('Global Temperature.csv')

natural_disaster_df['Latitude'],natural_disaster_df['Longitude'] = df_geoloc['Latitude'],df_geoloc['Longitude']
df_catastrophe_location = natural_disaster_df.dropna(subset=['Latitude', 'Longitude'])

annees = df_catastrophe_location['Year'].unique()

marqueur_type_de_catastrophe = {
    'Drought': {'color': 'beige', 'icon': 'tint'},
    'Drouuake': {'color': 'beige', 'icon': 'tint'},
    'Volcanic activity': {'color': 'orange', 'icon': 'fire'},
    'Mass movement (dry)': {'color': 'gray', 'icon': 'warning-sign'},
    'Storm': {'color': 'darkblue', 'icon': 'cloud'},
    'Earthquake': {'color': 'purple', 'icon': 'exclamation-sign'},
    'Earthquakeght': {'color': 'darkpurple', 'icon': 'exclamation-sign'},
    'Earthq':{'color': 'darkpurple', 'icon': 'exclamation-sign'},
    'Flood': {'color': 'blue', 'icon': 'tint'},
    'Epidemic': {'color': 'pink', 'icon': 'plus-sign'},
    'Landslide': {'color': 'darkgreen', 'icon': 'arrow-down'},
    'Wildfire': {'color': 'red', 'icon': 'fire'},
    'Extreme temperature ': {'color': 'darkred', 'icon': 'warning-sign'},
    'Fog': {'color': 'lightgray', 'icon': 'cloud'},
    'Insect infestation': {'color': 'green', 'icon': 'leaf'},
    'Impact': {'color': 'gray', 'icon': 'asterisk'},
    'Animal accident': {'color': 'green', 'icon': 'leaf'},
    'Glacial lake outburst': {'color': 'lightblue', 'icon': 'tint'}
}

    # dans config normalement

    ################################################
df_castrophe_country = natural_disaster_df.dropna(subset=['ISO','Year'])
disaster_counts = df_castrophe_country.groupby(['Year', 'ISO']).size().reset_index(name='Disaster Count')



disaster_death_counts = df_castrophe_country.groupby(['Year', 'ISO'])['Total Deaths'].sum().reset_index(name='Death Count')



# Chemin vers le fichier GeoJSON qui contient les frontières des pays
country_geojson = 'countries.geojson'  
    ################################################

