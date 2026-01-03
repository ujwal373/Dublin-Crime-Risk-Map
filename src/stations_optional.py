"""
Optional module for Garda station visualization and clustering.

This module handles station-level data when available.
Expected stations.csv format:
- station_name
- address
- lat
- lon
- garda_region
"""
import pandas as pd
import folium
from sklearn.cluster import DBSCAN
import numpy as np
from typing import Optional, Tuple


def load_stations_data(file_path: str) -> Optional[pd.DataFrame]:
    """
    Load Garda stations data from CSV.

    Args:
        file_path: Path to stations.csv

    Returns:
        DataFrame with station data or None if file doesn't exist
    """
    try:
        df = pd.read_csv(file_path)

        # Validate required columns
        required_cols = ['station_name', 'lat', 'lon', 'garda_region']
        if not all(col in df.columns for col in required_cols):
            print(f"Warning: stations.csv missing required columns: {required_cols}")
            return None

        # Drop rows with missing coordinates
        df = df.dropna(subset=['lat', 'lon'])

        return df

    except FileNotFoundError:
        return None
    except Exception as e:
        print(f"Error loading stations data: {e}")
        return None


def cluster_stations(stations_df: pd.DataFrame,
                     eps: float = 0.05,
                     min_samples: int = 2) -> pd.DataFrame:
    """
    Cluster stations using DBSCAN based on geographic proximity.

    Args:
        stations_df: DataFrame with station data
        eps: Maximum distance between stations in a cluster (in degrees)
        min_samples: Minimum number of stations to form a cluster

    Returns:
        DataFrame with added 'cluster' column
    """
    if len(stations_df) < min_samples:
        stations_df['cluster'] = 0
        return stations_df

    # Extract coordinates
    coords = stations_df[['lat', 'lon']].values

    # Perform DBSCAN clustering
    clustering = DBSCAN(eps=eps, min_samples=min_samples, metric='euclidean')
    stations_df['cluster'] = clustering.fit_predict(coords)

    return stations_df


def add_stations_to_map(m: folium.Map,
                        stations_df: pd.DataFrame,
                        zones_df: Optional[pd.DataFrame] = None) -> folium.Map:
    """
    Add station markers to an existing Folium map.

    Args:
        m: Folium map object
        stations_df: DataFrame with station data
        zones_df: Optional DataFrame with zone classifications for coloring

    Returns:
        Modified Folium map with station markers
    """
    # Create region-to-zone mapping if zones_df provided
    region_zones = {}
    if zones_df is not None:
        region_zones = dict(zip(zones_df['Garda Region'], zones_df['zone_color']))

    # Add markers for each station
    for idx, row in stations_df.iterrows():
        station_name = row['station_name']
        lat = row['lat']
        lon = row['lon']
        region = row.get('garda_region', 'Unknown')
        address = row.get('address', 'No address')

        # Determine marker color based on region zone
        marker_color = region_zones.get(region, 'blue')

        # Convert hex color to named color for folium
        color_map = {
            '#d73027': 'red',
            '#fee08b': 'orange',
            '#1a9850': 'green'
        }
        marker_color_name = color_map.get(marker_color, 'blue')

        # Create popup
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="margin: 0;">{station_name}</h4>
            <hr style="margin: 5px 0;">
            <b>Address:</b> {address}<br>
            <b>Region:</b> {region}<br>
        </div>
        """

        # Add marker
        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color=marker_color_name, icon='info-sign'),
            tooltip=station_name
        ).add_to(m)

    return m


def add_station_clusters_to_map(m: folium.Map,
                                stations_df: pd.DataFrame) -> folium.Map:
    """
    Add station cluster visualization to map.

    Args:
        m: Folium map object
        stations_df: DataFrame with station data and 'cluster' column

    Returns:
        Modified Folium map with cluster markers
    """
    if 'cluster' not in stations_df.columns:
        stations_df = cluster_stations(stations_df)

    # Get unique clusters (excluding noise points labeled as -1)
    clusters = stations_df[stations_df['cluster'] != -1]['cluster'].unique()

    # Color palette for clusters
    colors = ['red', 'blue', 'green', 'purple', 'orange', 'darkred',
              'lightred', 'beige', 'darkblue', 'darkgreen', 'cadetblue',
              'darkpurple', 'white', 'pink', 'lightblue', 'lightgreen']

    for cluster_id in clusters:
        stations_in_cluster = stations_df[stations_df['cluster'] == cluster_id]

        # Calculate cluster centroid
        centroid_lat = stations_in_cluster['lat'].mean()
        centroid_lon = stations_in_cluster['lon'].mean()

        color = colors[int(cluster_id) % len(colors)]

        # Add cluster marker
        folium.CircleMarker(
            location=[centroid_lat, centroid_lon],
            radius=15,
            popup=f'Cluster {cluster_id}<br>{len(stations_in_cluster)} stations',
            color=color,
            fill=True,
            fillColor=color,
            fillOpacity=0.6
        ).add_to(m)

        # Add markers for individual stations in cluster
        for idx, station in stations_in_cluster.iterrows():
            folium.CircleMarker(
                location=[station['lat'], station['lon']],
                radius=5,
                popup=station['station_name'],
                color=color,
                fill=True,
                fillColor=color,
                fillOpacity=0.8
            ).add_to(m)

    # Add noise points (cluster = -1) if any
    noise_stations = stations_df[stations_df['cluster'] == -1]
    for idx, station in noise_stations.iterrows():
        folium.CircleMarker(
            location=[station['lat'], station['lon']],
            radius=5,
            popup=station['station_name'],
            color='gray',
            fill=True,
            fillColor='gray',
            fillOpacity=0.5
        ).add_to(m)

    return m


def get_stations_in_region(stations_df: pd.DataFrame, region: str) -> pd.DataFrame:
    """
    Get all stations in a specific Garda region.

    Args:
        stations_df: DataFrame with station data
        region: Garda region name

    Returns:
        Filtered DataFrame with stations in the region
    """
    return stations_df[stations_df['garda_region'] == region]


def calculate_station_density(stations_df: pd.DataFrame) -> dict:
    """
    Calculate station density by region.

    Args:
        stations_df: DataFrame with station data

    Returns:
        dict mapping region to station count
    """
    return stations_df['garda_region'].value_counts().to_dict()
