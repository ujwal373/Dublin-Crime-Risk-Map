"""
Chart generation for crime data visualization.
"""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def create_trend_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create a line chart showing incident trends over quarters.

    Args:
        df: Filtered crime dataframe

    Returns:
        Plotly figure
    """
    # Aggregate by quarter
    trends = df.groupby('Quarter').agg({
        'VALUE': 'sum'
    }).reset_index()

    trends.columns = ['Quarter', 'Total Incidents']

    # Sort by quarter
    trends = trends.sort_values('Quarter')

    # Create line chart
    fig = px.line(
        trends,
        x='Quarter',
        y='Total Incidents',
        title='Crime Incidents Trend Over Time',
        markers=True
    )

    fig.update_layout(
        xaxis_title='Quarter',
        yaxis_title='Total Incidents',
        hovermode='x unified',
        template='plotly_white'
    )

    return fig


def create_top_offences_chart(top_offences_df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Create a horizontal bar chart of top offences.

    Args:
        top_offences_df: DataFrame with top offences
        top_n: Number of offences to show

    Returns:
        Plotly figure
    """
    data = top_offences_df.head(top_n).copy()

    fig = px.bar(
        data,
        x='total_incidents',
        y='Type of Offence',
        orientation='h',
        title=f'Top {top_n} Offence Types',
        color='total_incidents',
        color_continuous_scale='Reds'
    )

    fig.update_layout(
        xaxis_title='Total Incidents',
        yaxis_title='',
        yaxis={'categoryorder': 'total ascending'},
        template='plotly_white',
        showlegend=False
    )

    return fig


def create_region_risk_chart(risk_df: pd.DataFrame, top_n: int = 10) -> go.Figure:
    """
    Create a bar chart of top risky regions.

    Args:
        risk_df: DataFrame with risk scores
        top_n: Number of regions to show

    Returns:
        Plotly figure
    """
    data = risk_df.head(top_n).copy()

    # Color by zone
    color_map = {
        'Danger': '#d73027',
        'Warning': '#fee08b',
        'Safe': '#1a9850'
    }

    fig = px.bar(
        data,
        x='Garda Region',
        y='risk_score',
        title=f'Top {top_n} Risky Regions',
        color='zone',
        color_discrete_map=color_map,
        hover_data=['total_incidents']
    )

    fig.update_layout(
        xaxis_title='Garda Region',
        yaxis_title='Risk Score',
        xaxis_tickangle=-45,
        template='plotly_white'
    )

    return fig


def create_offence_category_pie(df: pd.DataFrame) -> go.Figure:
    """
    Create a pie chart showing distribution of offence categories.

    Args:
        df: Filtered crime dataframe

    Returns:
        Plotly figure
    """
    # Group by offence type
    offence_dist = df.groupby('Type of Offence').agg({
        'VALUE': 'sum'
    }).reset_index()

    offence_dist.columns = ['Type of Offence', 'Total']

    # Take top 10 and group rest as "Other"
    top_10 = offence_dist.nlargest(10, 'Total')
    other_sum = offence_dist[~offence_dist['Type of Offence'].isin(top_10['Type of Offence'])]['Total'].sum()

    if other_sum > 0:
        other_row = pd.DataFrame([{'Type of Offence': 'Other', 'Total': other_sum}])
        plot_data = pd.concat([top_10, other_row], ignore_index=True)
    else:
        plot_data = top_10

    fig = px.pie(
        plot_data,
        values='Total',
        names='Type of Offence',
        title='Offence Type Distribution',
        hole=0.3
    )

    fig.update_layout(template='plotly_white')

    return fig


def create_quarterly_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Create a heatmap showing incidents by region and quarter.

    Args:
        df: Filtered crime dataframe

    Returns:
        Plotly figure
    """
    # Aggregate by region and quarter
    heatmap_data = df.groupby(['Garda Region', 'Quarter']).agg({
        'VALUE': 'sum'
    }).reset_index()

    # Pivot for heatmap
    heatmap_pivot = heatmap_data.pivot(
        index='Garda Region',
        columns='Quarter',
        values='VALUE'
    ).fillna(0)

    fig = px.imshow(
        heatmap_pivot,
        labels=dict(x='Quarter', y='Garda Region', color='Incidents'),
        title='Crime Heatmap: Regions vs Quarters',
        aspect='auto',
        color_continuous_scale='YlOrRd'
    )

    fig.update_layout(template='plotly_white')

    return fig
