"""
Map visualization using Folium for Ireland crime risk.
"""
import folium
from folium import plugins
import pandas as pd
import numpy as np


# Approximate centroids for Irish Garda regions
# These are estimated coordinates - adjust based on actual boundaries
IRELAND_REGION_CENTROIDS = {
        # Dublin Metropolitan Region (DMR)
    "D.M.R. Eastern Garda Division": (53.3498, -6.2300),
    "D.M.R. North Central Garda Division": (53.3600, -6.2600),
    "D.M.R. Northern Garda Division": (53.3850, -6.2600),
    "D.M.R. South Central Garda Division": (53.3300, -6.2700),
    "D.M.R. Southern Garda Division": (53.3150, -6.2600),
    "D.M.R. Western Garda Division": (53.3450, -6.3100),

    # Leinster (outside DMR)
    "Cavan/Monaghan Garda Division": (54.0000, -7.3000),
    "Kildare Garda Division": (53.2200, -6.6600),
    "Kilkenny/Carlow Garda Division": (52.7200, -6.8500),
    "Laois/Offaly Garda Division": (53.0000, -7.4000),
    "Louth Garda Division": (53.9000, -6.5000),
    "Meath Garda Division": (53.6500, -6.7000),
    "Westmeath Garda Division": (53.5000, -7.3500),
    "Wexford Garda Division": (52.4500, -6.5000),
    "Wicklow Garda Division": (52.9800, -6.4600),

    # Munster
    "Cork City Garda Division": (51.8985, -8.4756),
    "Cork North Garda Division": (52.0500, -8.7000),
    "Cork West Garda Division": (51.6500, -9.2000),
    "Kerry Garda Division": (52.1500, -9.7000),
    "Limerick Garda Division": (52.6638, -8.6267),
    "Tipperary Garda Division": (52.6000, -7.9000),
    "Waterford Garda Division": (52.2593, -7.1101),

    # Connacht
    "Galway Garda Division": (53.2707, -9.0568),
    "Mayo Garda Division": (53.9000, -9.3500),
    "Roscommon/Longford Garda Division": (53.7000, -7.9000),

    # North-West
    "Donegal Garda Division": (54.8000, -8.0000),
    "Sligo/Leitrim Garda Division": (54.2000, -8.5000),
}


def get_region_coordinates(region_name: str) -> tuple:
    """
    Get coordinates for a Garda region.

    Args:
        region_name: Garda region name

    Returns:
        (latitude, longitude) tuple
    """
    # Try exact match first
    if region_name in IRELAND_REGION_CENTROIDS:
        return IRELAND_REGION_CENTROIDS[region_name]

    # Try partial match (case insensitive)
    region_lower = region_name.lower()
    for key, coords in IRELAND_REGION_CENTROIDS.items():
        if key.lower() in region_lower or region_lower in key.lower():
            return coords

    # Default to Ireland center
    return (53.4129, -8.2439)


def calculate_marker_radius(risk_score: float, min_radius: int = 300, max_radius: int = 2000) -> int:
    """
    Calculate circle marker radius based on risk score.

    Args:
        risk_score: Risk score for the region
        min_radius: Minimum radius in meters
        max_radius: Maximum radius in meters

    Returns:
        Radius in meters
    """
    # Will be normalized based on max risk score in the dataset
    return min_radius + int((max_radius - min_radius) * (risk_score / 1000))


def create_risk_map(zones_df: pd.DataFrame,
                    center_lat: float = 53.4129,
                    center_lon: float = -8.2439,
                    zoom_start: int = 7) -> folium.Map:
    """
    Create an interactive Folium map with risk zones.

    Args:
        zones_df: DataFrame with zone classifications
        center_lat: Map center latitude
        center_lon: Map center longitude
        zoom_start: Initial zoom level

    Returns:
        Folium Map object
    """
    # Create base map
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles='OpenStreetMap'
    )

    if len(zones_df) == 0:
        return m

    # Normalize risk scores for radius calculation
    max_risk = zones_df['risk_score'].max()
    min_risk = zones_df['risk_score'].min()

    # Add markers for each region
    for idx, row in zones_df.iterrows():
        region = row['Garda Region']
        risk_score = row['risk_score']
        zone = row['zone']
        zone_color = row['zone_color']
        total_incidents = row.get('total_incidents', 0)

        # Get coordinates
        lat, lon = get_region_coordinates(region)

        # Calculate radius (proportional to risk score)
        if max_risk > min_risk:
            normalized_risk = (risk_score - min_risk) / (max_risk - min_risk)
        else:
            normalized_risk = 0.5

        radius = 300 + (1500 * normalized_risk)

        # Create popup with detailed info
        popup_html = f"""
        <div style="font-family: Arial; width: 200px;">
            <h4 style="margin: 0; color: {zone_color};">{zone} Zone</h4>
            <hr style="margin: 5px 0;">
            <b>Region:</b> {region}<br>
            <b>Risk Score:</b> {risk_score:.1f}<br>
            <b>Total Incidents:</b> {int(total_incidents)}<br>
        </div>
        """

        # Add circle marker
        folium.Circle(
            location=[lat, lon],
            radius=radius,
            popup=folium.Popup(popup_html, max_width=250),
            color=zone_color,
            fill=True,
            fillColor=zone_color,
            fillOpacity=0.6,
            weight=2
        ).add_to(m)

        # Add a small marker at center
        folium.CircleMarker(
            location=[lat, lon],
            radius=5,
            color='black',
            fill=True,
            fillColor='white',
            fillOpacity=1,
            weight=1,
            popup=region
        ).add_to(m)

    # Add legend
    legend_html = """
    <div style="position: fixed;
                bottom: 50px; right: 50px; width: 180px; height: 120px;
                background-color: white; border:2px solid grey; z-index:9999;
                font-size:14px; padding: 10px">
        <p style="margin: 0; font-weight: bold;">Risk Zones</p>
        <hr style="margin: 5px 0;">
        <p style="margin: 5px 0;"><span style="color: #d73027;">&#9679;</span> Danger (High Risk)</p>
        <p style="margin: 5px 0;"><span style="color: #fee08b;">&#9679;</span> Warning (Medium Risk)</p>
        <p style="margin: 5px 0;"><span style="color: #1a9850;">&#9679;</span> Safe (Low Risk)</p>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    # Add fullscreen button
    plugins.Fullscreen().add_to(m)

    return m


def create_heatmap(zones_df: pd.DataFrame,
                   center_lat: float = 53.4129,
                   center_lon: float = -8.2439,
                   zoom_start: int = 7) -> folium.Map:
    """
    Create a heatmap visualization of crime risk.

    Args:
        zones_df: DataFrame with zone classifications
        center_lat: Map center latitude
        center_lon: Map center longitude
        zoom_start: Initial zoom level

    Returns:
        Folium Map object with heatmap layer
    """
    m = folium.Map(
        location=[center_lat, center_lon],
        zoom_start=zoom_start,
        tiles='OpenStreetMap'
    )

    if len(zones_df) == 0:
        return m

    # Prepare heat data
    heat_data = []
    for idx, row in zones_df.iterrows():
        lat, lon = get_region_coordinates(row['Garda Region'])
        # Weight by risk score
        heat_data.append([lat, lon, row['risk_score'] / 100])

    # Add heatmap layer with strong, visible colors
    plugins.HeatMap(
        heat_data,
        min_opacity=0.6,
        max_zoom=18,
        radius=30,
        blur=25,
        gradient={
            0.0: '#0d47a1',    # Dark blue (low risk)
            0.3: '#5e35b1',    # Deep purple
            0.5: '#e53935',    # Strong red
            0.7: '#ff6f00',    # Dark orange
            1.0: '#ffeb3b'     # Bright yellow (high risk)
        }
    ).add_to(m)

    # Add fullscreen button
    plugins.Fullscreen().add_to(m)

    return m


def add_region_labels(m: folium.Map, zones_df: pd.DataFrame) -> folium.Map:
    """
    Add text labels for regions on the map.

    Args:
        m: Folium map object
        zones_df: DataFrame with zone classifications

    Returns:
        Modified Folium map with labels
    """
    for idx, row in zones_df.iterrows():
        lat, lon = get_region_coordinates(row['Garda Region'])

        # Simplified region name for label
        label = row['Garda Region'].replace('Dublin Metropolitan Region', 'DMR').replace('10 ', '')

        folium.Marker(
            location=[lat, lon],
            icon=folium.DivIcon(html=f"""
                <div style="font-size: 10px; font-weight: bold;
                           background-color: white; padding: 2px 5px;
                           border: 1px solid black; border-radius: 3px;">
                    {label[:20]}
                </div>
            """)
        ).add_to(m)

    return m
