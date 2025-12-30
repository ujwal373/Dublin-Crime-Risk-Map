"""
Data loading and preprocessing for Dublin crime data.
"""
import pandas as pd
import re
from typing import Optional


def detect_delimiter(file_path: str) -> str:
    """
    Auto-detect delimiter (tab or comma) by reading first line.

    Args:
        file_path: Path to the data file

    Returns:
        str: Detected delimiter ('\\t' or ',')
    """
    with open(file_path, 'r', encoding='utf-8-sig') as f:
        first_line = f.readline()

    if '\t' in first_line:
        return '\t'
    return ','


def parse_quarter(quarter_str: str) -> Optional[pd.Period]:
    """
    Parse quarter string (e.g., '2023Q1') into a pandas Period.

    Args:
        quarter_str: Quarter string in format YYYYQN

    Returns:
        pd.Period or None if parsing fails
    """
    try:
        # Extract year and quarter number
        match = re.match(r'(\d{4})Q([1-4])', str(quarter_str))
        if match:
            year, quarter = match.groups()
            return pd.Period(f'{year}Q{quarter}', freq='Q')
    except:
        pass
    return None


def load_crime_data(file_path: str) -> pd.DataFrame:
    """
    Load crime data from TSV or CSV file.

    Expected columns:
    - Statistic Label
    - Quarter
    - Garda Region
    - Type of Offence
    - UNIT
    - VALUE

    Args:
        file_path: Path to crime data file

    Returns:
        pd.DataFrame with parsed and cleaned data
    """
    # Auto-detect delimiter
    delimiter = detect_delimiter(file_path)

    # Load data with BOM handling
    df = pd.read_csv(file_path, delimiter=delimiter, encoding='utf-8-sig')

    # Standardize column names (strip whitespace and remove BOM)
    df.columns = df.columns.str.strip().str.replace('\ufeff', '')

    # Parse quarter into sortable period
    df['Quarter_Parsed'] = df['Quarter'].apply(parse_quarter)

    # Convert VALUE to numeric, handling errors
    df['VALUE'] = pd.to_numeric(df['VALUE'], errors='coerce')

    # Drop rows with missing critical data
    df = df.dropna(subset=['Quarter_Parsed', 'Garda Region', 'Type of Offence', 'VALUE'])

    # Clean Garda Region names (strip whitespace)
    df['Garda Region'] = df['Garda Region'].str.strip()

    # Load ALL regions (not filtering by Dublin only)
    # Sort by quarter
    df = df.sort_values('Quarter_Parsed')

    return df


def get_available_quarters(df: pd.DataFrame) -> list:
    """
    Get sorted list of available quarters.

    Args:
        df: Crime dataframe

    Returns:
        List of quarter strings
    """
    return sorted(df['Quarter'].unique())


def get_available_regions(df: pd.DataFrame) -> list:
    """
    Get sorted list of available Garda regions.

    Args:
        df: Crime dataframe

    Returns:
        List of region names
    """
    return sorted(df['Garda Region'].unique())


def get_available_offences(df: pd.DataFrame) -> list:
    """
    Get sorted list of available offence types.

    Args:
        df: Crime dataframe

    Returns:
        List of offence types
    """
    return sorted(df['Type of Offence'].unique())


def filter_data(df: pd.DataFrame,
                quarters: Optional[list] = None,
                regions: Optional[list] = None,
                offences: Optional[list] = None) -> pd.DataFrame:
    """
    Filter crime data based on selected criteria.

    Args:
        df: Crime dataframe
        quarters: List of quarter strings to include
        regions: List of Garda regions to include
        offences: List of offence types to include

    Returns:
        Filtered dataframe
    """
    filtered = df.copy()

    if quarters:
        filtered = filtered[filtered['Quarter'].isin(quarters)]

    if regions:
        filtered = filtered[filtered['Garda Region'].isin(regions)]

    if offences:
        filtered = filtered[filtered['Type of Offence'].isin(offences)]

    return filtered
