import pandas as pd
import seaborn as sns
import random


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



# Sélectionner uniquement les colonnes nécessaires
selected_columns = ['Disaster Group', 'Disaster Subgroup', 'Disaster Type', 'Disaster Subtype', 'Disaster Subsubtype']
df_selected = natural_disaster_df[selected_columns]

# Créer la liste des labels
labels = pd.concat([df_selected[col] for col in selected_columns]).unique().tolist()

# Créer un mapping pour les labels
label_mapping = {label: idx for idx, label in enumerate(labels)}

# Initialiser les listes source, target et value
source = []
target = []
value = []

def fill_lists(df, col1, col2):
        
    grouped_df = df.groupby([col1, col2]).size().reset_index(name='count')
    for index, row in grouped_df.iterrows():
        source_idx = label_mapping[row[col1]]
        target_idx = label_mapping[row[col2]]
        source.append(source_idx)
        target.append(target_idx)
        value.append(row['count'])

# Remplir les listes pour chaque paire de colonnes adjacentes
for i in range(len(selected_columns) - 1):
    fill_lists(df_selected, selected_columns[i], selected_columns[i + 1])


# Generate a color palette with the same number of colors as there are labels
palette = sns.color_palette("husl", len(labels)).as_hex()

# Assign a color to each node
node_colors = [palette[i] for i in range(len(labels))]
# Générer des couleurs pour les liens
link_colors = [f'rgba({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)}, 0.5)' for _ in range(len(source))]

