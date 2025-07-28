# ⚾ Baseball Criteria Analyzer

A Streamlit web application that analyzes MLB games to find those meeting specific scoring criteria.

## 🎯 What it does

Finds MLB games that meet **Criteria X**:
- **7+ runs scored in the first 5 innings** AND 
- **Under 9 total runs for the entire game**

This identifies games with early offensive explosions that then became defensive battles.

## 🚀 Quick Start

### Option 1: Run Locally
```bash
git clone https://github.com/yourusername/baseball-criteria-analyzer
cd baseball-criteria-analyzer
pip install -r requirements.txt
streamlit run app.py
```

### Option 2: Deploy on Streamlit Cloud
1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub account
4. Deploy the app by selecting your forked repository

## 📊 Features

- **Real MLB Data**: Uses official MLB Stats API
- **Interactive Analysis**: Select seasons and customize analysis parameters
- **Visual Charts**: Pie charts and bar graphs showing results
- **Sample Games**: Detailed breakdown of games meeting criteria
- **Data Export**: Download results as CSV
- **Fast Mode**: Sample data option for quick testing

## 🎛️ Usage

1. **Select Season**: Choose from 2015-2025
2. **Choose Data Source**:
   - Live MLB API (real data, slower)
   - Sample data (demo mode, faster)
3. **Click "Analyze Games"**
4. **View Results**: Statistics, charts, and sample games
5. **Download Data**: Export matching games as CSV

## 📈 What You'll See

- **Total Games Analyzed**: Number of games processed
- **Matching Games**: Games meeting Criteria X
- **Match Rate**: Percentage of games meeting criteria
- **Visual Charts**: Data visualization
- **Game Details**: Inning-by-inning breakdowns

## 🔧 Technical Details

- **Framework**: Streamlit
- **Data Source**: MLB Stats API
- **Caching**: Results cached for 1 hour
- **Rate Limiting**: API calls throttled to be respectful
- **Fallback**: Sample data if API fails

## 📝 Files Structure

```
baseball-criteria-analyzer/
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── .streamlit/
    └── config.toml    # Streamlit configuration
```

## 🌐 Live Demo

[View Live App](https://your-app-name.streamlit.app) (replace with your deployed URL)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🏟️ Baseball Stats Explained

**Criteria X Analysis**: This unique criteria identifies games where teams scored heavily early (7+ runs in first 5 innings) but the game stayed relatively low-scoring overall (under 9 total runs). These games represent interesting scenarios where early offensive outbursts were followed by strong defensive performances or pitching changes.

## 🐛 Issues & Support

If you encounter any issues or have suggestions:
1. Check the [Issues](https://github.com/yourusername/baseball-criteria-analyzer/issues) page
2. Create a new issue if your problem isn't already listed
3. Provide as much detail as possible

## 🎯 Future Enhancements

- [ ] Multiple criteria analysis
- [ ] Team-specific filtering
- [ ] Historical trend analysis
- [ ] Advanced visualizations
- [ ] Mobile optimization
- [ ] Real-time game tracking

---

Made with ⚾ and ❤️ using Streamlit