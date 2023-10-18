Code permettant d'obbtenir les longitutes et les latitudes des localisation du data frame.


import pandas as pd
import concurrent.futures
from geopy.geocoders import GoogleV3
from geopy.extra.rate_limiter import RateLimiter

# Charger le fichier CSV
df = pd.read_csv("1900_2021_DISASTERS.xlsx - emdat data.csv")

# Imprimer le nombre de valeurs manquantes dans la colonne 'Latitude'
print(df['Latitude'].isna().sum())

# Initialiser le géolocalisateur
geolocator = GoogleV3(api_key="AIzaSyBDLRfAKkVqy7HUO49RSpRsleMUVIP7How")
geocode = RateLimiter(geolocator.geocode, min_delay_seconds=1/50)

# Créer un dictionnaire de cache
cache = {}

def get_coordinates(address):
    # Si l'adresse est dans le cache, retourner le résultat en cache
    if address in cache:
        return cache[address]

    # Sinon, obtenir les coordonnées de l'API
    location = geocode(address)
    if location is not None:
        coordinates = (location.latitude, location.longitude)
    else:
        coordinates = (None, None)

    # Stocker le résultat dans le cache
    cache[address] = coordinates

    return coordinates

# Appliquer la fonction à chaque ligne du dataframe en parallèle
with concurrent.futures.ThreadPoolExecutor() as executor:
    df['Latitude'], df['Longitude'] = zip(*executor.map(get_coordinates, df['Location']))

# Imprimer le nombre de valeurs manquantes dans la colonne 'Latitude' après géocodage
print(df['Latitude'].isna().sum())

# Conserver uniquement les colonnes 'Location', 'Latitude' et 'Longitude'
df = df[['Location', 'Latitude', 'Longitude']]

# Sauvegarder le nouveau dataframe dans un fichier CSV
df.to_csv("new_dataframe.csv", index=False)
