"""
Risk scoring logic for crime data.
"""
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path for config imports
sys.path.append(str(Path(__file__).parent.parent))
from config.severity_weights import get_offence_weight


def calculate_risk_scores(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate risk scores for each region based on crime data.

    Risk score = sum(VALUE * severity_weight) for each region.

    Args:
        df: Filtered crime dataframe

    Returns:
        DataFrame with columns: ['Garda Region', 'risk_score', 'total_incidents']
    """
    # Create a copy with severity weights
    df_scored = df.copy()
    df_scored['severity_weight'] = df_scored['Type of Offence'].apply(get_offence_weight)

    # Calculate weighted score
    df_scored['weighted_score'] = df_scored['VALUE'] * df_scored['severity_weight']

    # Aggregate by region
    risk_by_region = df_scored.groupby('Garda Region').agg({
        'weighted_score': 'sum',
        'VALUE': 'sum'
    }).reset_index()

    risk_by_region.columns = ['Garda Region', 'risk_score', 'total_incidents']

    # Sort by risk score descending
    risk_by_region = risk_by_region.sort_values('risk_score', ascending=False)

    return risk_by_region


def get_top_risky_regions(risk_df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Get top N risky regions.

    Args:
        risk_df: Risk scores dataframe
        top_n: Number of top regions to return

    Returns:
        DataFrame with top risky regions
    """
    return risk_df.head(top_n)


def get_top_offences(df: pd.DataFrame, top_n: int = 10) -> pd.DataFrame:
    """
    Get top N offence types by total incidents.

    Args:
        df: Filtered crime dataframe
        top_n: Number of top offences to return

    Returns:
        DataFrame with columns: ['Type of Offence', 'total_incidents']
    """
    top_offences = df.groupby('Type of Offence').agg({
        'VALUE': 'sum'
    }).reset_index()

    top_offences.columns = ['Type of Offence', 'total_incidents']
    top_offences = top_offences.sort_values('total_incidents', ascending=False)

    return top_offences.head(top_n)


def calculate_offence_breakdown(df: pd.DataFrame, region: str) -> pd.DataFrame:
    """
    Calculate offence breakdown for a specific region.

    Args:
        df: Filtered crime dataframe
        region: Garda region name

    Returns:
        DataFrame with offence breakdown
    """
    region_data = df[df['Garda Region'] == region]

    breakdown = region_data.groupby('Type of Offence').agg({
        'VALUE': 'sum'
    }).reset_index()

    breakdown.columns = ['Type of Offence', 'incidents']
    breakdown = breakdown.sort_values('incidents', ascending=False)

    return breakdown
