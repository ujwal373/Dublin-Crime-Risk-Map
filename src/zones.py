"""
Zone classification (Safe, Warning, Danger) based on risk scores.
"""
import pandas as pd
import numpy as np


class ZoneConfig:
    """Configuration for zone thresholds."""

    def __init__(self,
                 danger_percentile: float = 80,
                 warning_percentile: float = 50):
        """
        Initialize zone configuration.

        Args:
            danger_percentile: Top percentile for Danger zone (default 80 = top 20%)
            warning_percentile: Percentile for Warning zone start (default 50 = middle 30%)
        """
        self.danger_percentile = danger_percentile
        self.warning_percentile = warning_percentile

    def get_thresholds(self, risk_scores: pd.Series) -> dict:
        """
        Calculate threshold values based on risk score distribution.

        Args:
            risk_scores: Series of risk scores

        Returns:
            dict with 'danger' and 'warning' threshold values
        """
        if len(risk_scores) == 0:
            return {'danger': 0, 'warning': 0}

        danger_threshold = np.percentile(risk_scores, self.danger_percentile)
        warning_threshold = np.percentile(risk_scores, self.warning_percentile)

        return {
            'danger': danger_threshold,
            'warning': warning_threshold
        }


def classify_zones(risk_df: pd.DataFrame,
                   zone_config: ZoneConfig = None) -> pd.DataFrame:
    """
    Classify regions into Safe, Warning, or Danger zones.

    Args:
        risk_df: DataFrame with risk scores (from scoring.calculate_risk_scores)
        zone_config: ZoneConfig instance (uses default if None)

    Returns:
        DataFrame with added 'zone' and 'zone_color' columns
    """
    if zone_config is None:
        zone_config = ZoneConfig()

    df = risk_df.copy()

    # Calculate thresholds
    thresholds = zone_config.get_thresholds(df['risk_score'])

    # Classify zones
    def get_zone(risk_score):
        if risk_score >= thresholds['danger']:
            return 'Danger'
        elif risk_score >= thresholds['warning']:
            return 'Warning'
        else:
            return 'Safe'

    df['zone'] = df['risk_score'].apply(get_zone)

    # Add color coding
    zone_colors = {
        'Danger': '#d73027',    # Red
        'Warning': '#fee08b',   # Yellow
        'Safe': '#1a9850'       # Green
    }
    df['zone_color'] = df['zone'].map(zone_colors)

    return df


def get_zone_statistics(zones_df: pd.DataFrame) -> dict:
    """
    Get statistics about zone distribution.

    Args:
        zones_df: DataFrame with zone classifications

    Returns:
        dict with zone counts and percentages
    """
    total_regions = len(zones_df)

    zone_counts = zones_df['zone'].value_counts().to_dict()

    stats = {
        'total_regions': total_regions,
        'counts': zone_counts,
        'percentages': {
            zone: (count / total_regions * 100) if total_regions > 0 else 0
            for zone, count in zone_counts.items()
        }
    }

    return stats


def get_regions_by_zone(zones_df: pd.DataFrame, zone: str) -> list:
    """
    Get list of regions in a specific zone.

    Args:
        zones_df: DataFrame with zone classifications
        zone: Zone name ('Safe', 'Warning', or 'Danger')

    Returns:
        List of region names
    """
    return zones_df[zones_df['zone'] == zone]['Garda Region'].tolist()
