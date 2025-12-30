# Quick Start Guide

Get your Dublin Crime Risk Visualization app running in 5 minutes!

## 🚀 Fast Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the app
streamlit run app.py
```

## 📊 Using the App

1. **Open browser** - App opens at `http://localhost:8501`

2. **Upload data** - Click "Browse files" in sidebar
   - Use provided `data/sample_crime_data.csv` to test
   - Or upload your own crime data (CSV/TSV)

3. **Explore**:
   - 🗺️ **Map** - View risk zones (green=safe, yellow=warning, red=danger)
   - 🔍 **Filters** - Select quarters, regions, offence types
   - 📈 **Charts** - See trends and top offences
   - 🎓 **Alerts** - Check top risky regions

## 🎯 Sample Data Included

Try the app with included sample data:
- `data/sample_crime_data.csv` - Example crime statistics
- `data/sample_stations.csv` - Example Garda stations

## ⚙️ Customization

### Adjust Risk Zones
Use sidebar sliders:
- **Danger Zone**: Top % classified as high risk (default: 80%)
- **Warning Zone**: Middle % classified as medium risk (default: 50%)

### Change Severity Weights
Edit `config/severity_weights.py`:
```python
SEVERITY_WEIGHTS = {
    'murder': 5,    # Highest
    'assault': 4,
    'burglary': 3,
    'theft': 2,
    'minor': 1      # Lowest
}
```

## 🌐 Deploy Online

### Option 1: Streamlit Community Cloud (Free)
1. Push code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repo
4. Deploy!

Detailed instructions in [README.md](README.md)

## 📁 Your Data Format

Required columns in CSV/TSV:
```
Statistic Label | Quarter | Garda Region | Type of Offence | UNIT | VALUE
```

Example:
```csv
Recorded Crime Incidents,2023Q1,10 Dublin Metropolitan Region,Murder (0111),Number,2
Recorded Crime Incidents,2023Q1,Dublin Metropolitan Region North,Assault,Number,145
```

## 🆘 Troubleshooting

**App won't start?**
- Check Python version: `python --version` (need 3.8+)
- Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

**Data won't load?**
- Verify columns match expected format
- Check "Garda Region" contains "Dublin"
- Ensure "Quarter" is formatted like "2023Q1"

**Map not showing?**
- Refresh browser
- Try different browser
- Check browser console (F12) for errors

## 📚 More Help

- Full documentation: [README.md](README.md)
- Streamlit docs: [docs.streamlit.io](https://docs.streamlit.io)

---

**Ready to explore Dublin crime data? Run `streamlit run app.py` and start!**
