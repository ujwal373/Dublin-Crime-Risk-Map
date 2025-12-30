# Dublin Crime Risk Visualization

An interactive Streamlit dashboard for analyzing and visualizing crime risk across Dublin Garda regions. This application helps students and residents understand crime patterns and assess safety levels in different areas.

## Features

- **Interactive Risk Map**: Visualize crime risk zones (Safe, Warning, Danger) across Dublin Garda regions
- **Dynamic Filtering**: Filter by quarter range, regions, and offence types
- **Risk Scoring**: Severity-weighted risk calculation based on offence types
- **Student Alerts**: Quick view of top risky regions and most common offences
- **Trend Analysis**: Charts showing crime trends over time
- **Station Support**: Optional Garda station visualization with clustering
- **Customizable Thresholds**: Adjust risk zone percentiles

## Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

## Installation

### Local Setup

1. **Clone or download this repository**

2. **Navigate to the project directory**
   ```bash
   cd dublin-crime-risk
   ```

3. **Create a virtual environment (recommended)**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate

   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running Locally

1. **Activate virtual environment** (if not already activated)
   ```bash
   # Windows
   venv\Scripts\activate

   # macOS/Linux
   source venv/bin/activate
   ```

2. **Run the Streamlit app**
   ```bash
   streamlit run app.py
   ```

3. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If it doesn't open automatically, navigate to the URL shown in the terminal

4. **Upload your data**
   - Use the sidebar file uploader to upload your crime data (CSV/TSV)
   - Optionally upload stations.csv for station visualization

## Data Format

### Crime Data (Required)

Your crime data file should be a CSV or TSV with the following columns:

| Column | Description | Example |
|--------|-------------|---------|
| Statistic Label | Description of the statistic | "Recorded Crime Incidents" |
| Quarter | Time period | "2023Q1" |
| Garda Region | Dublin region name | "10 Dublin Metropolitan Region" |
| Type of Offence | Crime category | "Murder (0111)" |
| UNIT | Measurement unit | "Number" |
| VALUE | Numeric incident count | 42 |

Example:
```csv
Statistic Label,Quarter,Garda Region,Type of Offence,UNIT,VALUE
Recorded Crime Incidents,2023Q1,10 Dublin Metropolitan Region,Murder (0111),Number,2
Recorded Crime Incidents,2023Q1,10 Dublin Metropolitan Region,Assault,Number,145
```

### Stations Data (Optional)

If you have Garda station data, create a `stations.csv` file with:

| Column | Description | Example |
|--------|-------------|---------|
| station_name | Station name | "Pearse Street Garda Station" |
| address | Full address | "Pearse Street, Dublin 2" |
| lat | Latitude | 53.3438 |
| lon | Longitude | -6.2438 |
| garda_region | Associated region | "DMR Eastern" |

## Deployment to Streamlit Community Cloud

### Step 1: Prepare Your Repository

1. **Create a GitHub account** (if you don't have one)
   - Go to [github.com](https://github.com) and sign up

2. **Create a new repository**
   - Click "New repository"
   - Name it (e.g., "dublin-crime-risk")
   - Set to Public
   - Click "Create repository"

3. **Push your code to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/YOUR_USERNAME/dublin-crime-risk.git
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Community Cloud

1. **Go to [share.streamlit.io](https://share.streamlit.io)**

2. **Sign in with GitHub**

3. **Click "New app"**

4. **Fill in deployment details**:
   - Repository: Select your repository (e.g., `YOUR_USERNAME/dublin-crime-risk`)
   - Branch: `main`
   - Main file path: `app.py`

5. **Click "Deploy"**
   - The app will build and deploy automatically
   - You'll receive a URL like `https://YOUR_USERNAME-dublin-crime-risk.streamlit.app`

6. **Share your app**
   - The URL is now publicly accessible
   - Users can upload their own crime data files

### Step 3: Update Your App

To update your deployed app:

```bash
git add .
git commit -m "Update description"
git push
```

Streamlit Community Cloud will automatically redeploy your app.

## Configuration

### Adjusting Severity Weights

Edit `config/severity_weights.py` to customize how different crime types are weighted:

```python
SEVERITY_WEIGHTS = {
    'murder': 5,      # Highest severity
    'assault': 4,     # High severity
    'burglary': 3,    # Medium-high
    'theft': 2,       # Medium
    'minor': 1,       # Low severity
}
```

### Adjusting Region Coordinates

If you have more accurate coordinates for Dublin Garda regions, edit `src/viz_map.py`:

```python
DUBLIN_REGION_CENTROIDS = {
    'Your Region Name': (latitude, longitude),
    ...
}
```

## Project Structure

```
dublin-crime-risk/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── config/
│   └── severity_weights.py    # Crime severity configuration
├── src/
│   ├── __init__.py
│   ├── data_loader.py         # Data loading and preprocessing
│   ├── scoring.py             # Risk scoring logic
│   ├── zones.py               # Zone classification
│   ├── viz_map.py             # Map visualization
│   ├── charts.py              # Chart generation
│   └── stations_optional.py   # Station visualization (optional)
└── data/
    └── .gitkeep               # Placeholder for data files
```

## Usage Tips

1. **Filtering**: Use the sidebar filters to focus on specific time periods, regions, or offence types
2. **Zone Thresholds**: Adjust the danger and warning percentiles to customize risk classification
3. **Map Types**: Switch between "Risk Zones" (colored circles) and "Heatmap" views
4. **Student Alerts**: Check the top 10 risky regions for quick safety insights
5. **Charts**: Explore different tabs to see trends, offence distributions, and heatmaps

## Troubleshooting

### App won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### Data not loading
- Verify your CSV/TSV has the required columns
- Check that "Garda Region" contains "Dublin" in the name
- Ensure "Quarter" follows the format YYYYQ# (e.g., 2023Q1)

### Map not displaying
- Clear browser cache and refresh
- Check browser console for errors
- Ensure coordinates in viz_map.py are valid

### Deployment fails
- Verify requirements.txt is in the root directory
- Check that all imports are available in requirements.txt
- Review Streamlit Cloud logs for specific errors

## Contributing

To extend this project:

1. Add new chart types in `src/charts.py`
2. Implement additional risk scoring methods in `src/scoring.py`
3. Add custom map layers in `src/viz_map.py`
4. Enhance filtering options in `app.py`

## Data Sources

This application is designed to work with crime statistics data. Typical sources include:

- Central Statistics Office (CSO) Ireland
- Garda Síochána crime statistics
- Local government crime reports

Ensure you have permission to use any data you upload.

## License

This project is provided as-is for educational and research purposes.

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)
3. Check Folium documentation: [python-visualization.github.io/folium](https://python-visualization.github.io/folium/)

---

Built with Streamlit, Folium, and Plotly
