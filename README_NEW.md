# Ireland Crime Risk Visualization

An interactive Streamlit dashboard for analyzing and visualizing crime risk across all Irish Garda regions using official government crime data.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- `crimedata.csv` file (from Irish Government statistics)

### Installation

1. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Ensure data file is present**
   - Place your `crimedata.csv` file in the project root directory
   - The file is automatically loaded on startup

3. **Run the application**
   ```bash
   streamlit run app.py
   ```

4. **Access the dashboard**
   - Open your browser to `http://localhost:8501`
   - The app will automatically load and display all regions

## 📊 Features

### Automatic Data Loading
- **No manual upload required** - App loads `crimedata.csv` directly from root directory
- **All regions supported** - Displays all 4 Irish Garda regions:
  - 10 Dublin Metropolitan Region
  - 20 North Western Region
  - 30 Eastern Region
  - 40 Southern Region

### Interactive Visualization
- **Risk Map** - Color-coded zones (Safe/Warning/Danger) for all regions
- **Heatmap View** - Alternative visualization showing crime intensity
- **Dynamic Filtering** - Filter by:
  - Quarter range (time periods)
  - Specific Garda regions
  - Types of offences

### Risk Analysis
- **Smart Risk Scoring** - Severity-weighted by offence type
- **Customizable Zones** - Adjust danger/warning thresholds via sliders
- **Top Alerts** - Quick view of highest-risk regions and most common offences

### Analytics Dashboard
- **Trend Charts** - Crime incidents over time
- **Offence Analysis** - Top crime types by region
- **Region Comparison** - Risk scores across all regions
- **Heatmaps** - Regions vs quarters visualization

## 📁 Required Data Format

Your `crimedata.csv` should have these columns:

| Column | Description | Example |
|--------|-------------|---------|
| Statistic Label | Description | "Recorded crime incidents" |
| Quarter | Time period | "2023Q1" |
| Garda Region | Region name | "10 Dublin Metropolitan Region" |
| Type of Offence | Crime category | "Assault causing harm (0211)" |
| UNIT | Measurement | "Number" |
| VALUE | Incident count | 145 |

Example:
```csv
Statistic Label,Quarter,Garda Region,Type of Offence,UNIT,VALUE
Recorded crime incidents,2023Q1,10 Dublin Metropolitan Region,Murder (0111),Number,3
Recorded crime incidents,2023Q1,20 North Western Region,Assault causing harm,Number,267
```

## 🎯 Using the Dashboard

### Sidebar Controls
1. **Data Status** - Shows loaded records, regions, and quarters
2. **Filters Section**:
   - Adjust quarter range slider
   - Select specific regions
   - Choose offence types
3. **Zone Thresholds**:
   - Danger Zone (default: top 20%)
   - Warning Zone (default: middle 30%)
4. **Map Options**:
   - Toggle between Risk Zones and Heatmap
   - Optional station markers (if available)

### Main Dashboard
- **Interactive Map** - Pan, zoom, click markers for details
- **Zone Statistics** - Current distribution of Safe/Warning/Danger zones
- **Student Alerts** - Top 10 risky regions and offences
- **Charts Section** - Multiple tabs with different visualizations

## ⚙️ Configuration

### Adjusting Crime Severity Weights

Edit `config/severity_weights.py` to customize risk scoring:

```python
SEVERITY_WEIGHTS = {
    'murder': 5,      # Highest severity
    'assault': 4,
    'burglary': 3,
    'theft': 2,
    'minor': 1        # Lowest severity
}
```

### Region Coordinates

Region centroids are defined in `src/viz_map.py`. Current locations:
- Dublin Metropolitan: (53.3498, -6.2603)
- North Western: (54.4500, -8.2500)
- Eastern: (53.6500, -7.2500)
- Southern: (52.2500, -8.5000)

Adjust these if you have more precise coordinates.

## 📂 Project Structure

```
crime-project/
├── app.py                      # Main Streamlit application
├── crimedata.csv              # Your crime data (required)
├── requirements.txt           # Python dependencies
├── README_NEW.md             # This file
├── config/
│   └── severity_weights.py   # Crime severity configuration
├── src/
│   ├── data_loader.py        # Data loading (handles BOM, all regions)
│   ├── scoring.py            # Risk scoring logic
│   ├── zones.py              # Zone classification
│   ├── viz_map.py            # Map visualization (all Ireland)
│   ├── charts.py             # Chart generation
│   └── stations_optional.py  # Optional station support
└── data/
    └── sample_stations.csv   # Optional station data
```

## 🔧 Troubleshooting

### "Crime data file not found!"
- Ensure `crimedata.csv` is in the project root directory (same folder as `app.py`)

### "Only showing one region"
- This has been fixed! The app now loads all regions automatically
- Check that your CSV has multiple regions (10, 20, 30, 40)

### Data not loading properly
- Check CSV encoding (should be UTF-8)
- Verify column names match expected format
- Ensure "Quarter" column has format like "2023Q1"

### Map not showing all regions
- The app now centers on all of Ireland (zoom level 7)
- All 4 regions should be visible on the map
- Click region markers for detailed information

## 📊 Data Source

This application is designed to work with crime statistics from:
- **Central Statistics Office (CSO) Ireland**
- **Garda Síochána crime statistics**
- **Irish Government open data portal**

Ensure you have permission to use any data you process.

## 🌐 Deployment

### Streamlit Community Cloud (Free)

1. Push code to GitHub:
   ```bash
   git add .
   git commit -m "Ireland crime visualization app"
   git push origin main
   ```

2. Go to [share.streamlit.io](https://share.streamlit.io)

3. Connect your repository and deploy

4. **Important**: Upload your `crimedata.csv` to the repository (ensure it's not too large)

### Local Network Deployment

Run with external access:
```bash
streamlit run app.py --server.address=0.0.0.0
```

## 📝 Key Changes from Original

### What Changed
1. ✅ **Auto-loads** `crimedata.csv` from root directory
2. ✅ **All regions** now loaded (not just Dublin)
3. ✅ **Fixed BOM encoding** issues in CSV reading
4. ✅ **Updated map center** to show all of Ireland
5. ✅ **Added region coordinates** for all 4 Garda regions
6. ✅ **No file upload** required - uses local file directly

### Benefits
- **No schema disruption** - Users can't upload incorrect formats
- **Faster startup** - Data pre-loaded, no upload delays
- **More reliable** - Single source of truth for data
- **Complete coverage** - All Irish regions visible

## 💡 Tips

1. **First Time Use**: Let all regions load, then explore filters
2. **Performance**: For faster loading, filter by specific quarters
3. **Analysis**: Use heatmap view to spot temporal patterns
4. **Comparison**: Select specific regions to compare risk scores
5. **Export**: Use the data table view to see detailed statistics

## 📧 Support

For issues:
1. Check that `crimedata.csv` is in the correct location
2. Verify CSV format matches expected structure
3. Review Streamlit documentation: [docs.streamlit.io](https://docs.streamlit.io)

## 📜 License

This project is provided for educational and analytical purposes.

---

**Built with Streamlit, Folium, Plotly, and Pandas**

Last Updated: 2025
