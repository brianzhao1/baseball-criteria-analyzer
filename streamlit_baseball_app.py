# File: app.py
import streamlit as st
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import time

# Page config
st.set_page_config(
    page_title="⚾ Baseball Criteria Analyzer",
    page_icon="⚾",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .criteria-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        text-align: center;
        font-size: 1.2rem;
        font-weight: bold;
    }
    .metric-card {
        background: #f8f9fa;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
    }
    .game-card {
        background: #ffffff;
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 1rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def get_season_games(year, max_days=30):
    """
    Collect MLB games for a season (limited sample for demo)
    """
    start_date = f"{year}-04-01"
    all_games = []
    current_date = datetime.strptime(start_date, "%Y-%m-%d")
    days_processed = 0
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    while days_processed < max_days:
        date_str = current_date.strftime("%Y-%m-%d")
        
        try:
            url = f"https://statsapi.mlb.com/api/v1/schedule?sportId=1&date={date_str}&hydrate=linescore"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if 'dates' in data and len(data['dates']) > 0:
                    games = data['dates'][0].get('games', [])
                    
                    for game in games:
                        if game.get('status', {}).get('detailedState') == 'Final':
                            game_data = extract_game_data(game)
                            if game_data:
                                all_games.append(game_data)
            
            days_processed += 1
            progress_bar.progress(days_processed / max_days)
            status_text.text(f"Processing {date_str}... ({len(all_games)} games found)")
            
        except Exception as e:
            st.error(f"Error processing {date_str}: {e}")
        
        current_date += timedelta(days=3)  # Skip every 3rd day for faster processing
        time.sleep(0.1)
    
    progress_bar.empty()
    status_text.empty()
    
    return all_games

def extract_game_data(game):
    """Extract relevant data from MLB API game object"""
    try:
        linescore = game.get('linescore', {})
        innings = linescore.get('innings', [])
        
        if not innings:
            return None
        
        game_data = {
            'date': game.get('gameDate', ''),
            'game_id': game.get('gamePk', ''),
            'away_team': game.get('teams', {}).get('away', {}).get('team', {}).get('name', ''),
            'home_team': game.get('teams', {}).get('home', {}).get('team', {}).get('name', ''),
            'away_score': game.get('teams', {}).get('away', {}).get('score', 0),
            'home_score': game.get('teams', {}).get('home', {}).get('score', 0),
            'innings': []
        }
        
        for i, inning in enumerate(innings):
            inning_data = {
                'inning': i + 1,
                'away_runs': inning.get('away', {}).get('runs', 0) or 0,
                'home_runs': inning.get('home', {}).get('runs', 0) or 0
            }
            game_data['innings'].append(inning_data)
        
        return game_data
        
    except Exception:
        return None

def meets_criteria_x(game_data):
    """Check if game meets Criteria X: 7+ runs in first 5 innings AND under 9 total runs"""
    if not game_data or not game_data['innings']:
        return False
    
    runs_first_5 = sum(inning['away_runs'] + inning['home_runs'] 
                      for inning in game_data['innings'][:5])
    total_runs = game_data['away_score'] + game_data['home_score']
    
    return runs_first_5 >= 7 and total_runs < 9

def meets_criteria_y(game_data):
    """Check if game meets Criteria Y: 6+ runs in first 5 innings AND 9 or fewer total runs"""
    if not game_data or not game_data['innings']:
        return False
    
    runs_first_5 = sum(inning['away_runs'] + inning['home_runs'] 
                      for inning in game_data['innings'][:5])
    total_runs = game_data['away_score'] + game_data['home_score']
    
    return runs_first_5 >= 6 and total_runs <= 9

def get_sample_data():
    """Fallback sample data if API fails"""
    return [
        {
            'date': '2024-05-15',
            'away_team': 'Boston Red Sox',
            'home_team': 'New York Yankees',
            'away_score': 5,
            'home_score': 3,
            'innings': [
                {'inning': 1, 'away_runs': 2, 'home_runs': 1},
                {'inning': 2, 'away_runs': 1, 'home_runs': 2},
                {'inning': 3, 'away_runs': 2, 'home_runs': 0},
                {'inning': 4, 'away_runs': 0, 'home_runs': 0},
                {'inning': 5, 'away_runs': 0, 'home_runs': 0},
                {'inning': 6, 'away_runs': 0, 'home_runs': 0},
                {'inning': 7, 'away_runs': 0, 'home_runs': 0},
                {'inning': 8, 'away_runs': 0, 'home_runs': 0},
                {'inning': 9, 'away_runs': 0, 'home_runs': 0}
            ]
        },
        {
            'date': '2024-06-22',
            'away_team': 'Chicago Cubs',
            'home_team': 'St. Louis Cardinals',
            'away_score': 4,
            'home_score': 4,
            'innings': [
                {'inning': 1, 'away_runs': 2, 'home_runs': 1},
                {'inning': 2, 'away_runs': 1, 'home_runs': 2},
                {'inning': 3, 'away_runs': 1, 'home_runs': 1},
                {'inning': 4, 'away_runs': 0, 'home_runs': 0},
                {'inning': 5, 'away_runs': 0, 'home_runs': 0},
                {'inning': 6, 'away_runs': 0, 'home_runs': 0},
                {'inning': 7, 'away_runs': 0, 'home_runs': 0},
                {'inning': 8, 'away_runs': 0, 'home_runs': 0},
                {'inning': 9, 'away_runs': 0, 'home_runs': 0}
            ]
        }
    ] * 25  # Multiply to simulate more games

def main():
    # Header
    st.markdown('<div class="main-header">⚾ Baseball Criteria Analyzer</div>', unsafe_allow_html=True)
    
    # Criteria explanation
    st.markdown("""
    <div class="criteria-box">
        <strong>Criteria X:</strong> Games with 7+ runs in first 5 innings AND under 9 total runs<br>
        <strong>Criteria Y:</strong> Games with 6+ runs in first 5 innings AND 9 or fewer total runs
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    st.sidebar.header("🎛️ Controls")
    
    # Season selection
    current_year = datetime.now().year
    season = st.sidebar.selectbox(
        "Select Season",
        options=list(range(current_year, 2014, -1)),
        index=1 if current_year > 2024 else 0
    )
    
    # Data source selection
    use_live_data = st.sidebar.checkbox("Use Live MLB API", value=False, help="Uncheck to use sample data (faster)")
    
    if use_live_data:
        max_days = st.sidebar.slider("Days to analyze", 10, 60, 30, help="More days = more accurate but slower")
    
    # Analyze button
    if st.sidebar.button("🔍 Analyze Games", type="primary"):
        st.subheader(f"📊 Analyzing {season} Season...")
        
        # Get games data
        with st.spinner("Collecting game data..."):
            if use_live_data:
                try:
                    games = get_season_games(season, max_days)
                except Exception as e:
                    st.error(f"API Error: {e}")
                    st.info("Falling back to sample data...")
                    games = get_sample_data()
            else:
                games = get_sample_data()
        
        if not games:
            st.error("No games found for the selected criteria.")
            return
        
        # Analyze games
        total_games = len(games)
        criteria_x_games = [game for game in games if meets_criteria_x(game)]
        criteria_y_games = [game for game in games if meets_criteria_y(game)]
        
        # Remove Criteria X games from Criteria Y to avoid double counting
        criteria_y_only = [game for game in criteria_y_games if not meets_criteria_x(game)]
        
        x_count = len(criteria_x_games)
        y_count = len(criteria_y_only)
        total_matching = x_count + y_count
        
        x_percentage = (x_count / total_games * 100) if total_games > 0 else 0
        y_percentage = (y_count / total_games * 100) if total_games > 0 else 0
        total_percentage = (total_matching / total_games * 100) if total_games > 0 else 0
        
        # Display results
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                label="📈 Total Games",
                value=f"{total_games:,}",
                help="Total number of games analyzed"
            )
        
        with col2:
            st.metric(
                label="🎯 Criteria X",
                value=f"{x_count:,}",
                delta=f"{x_percentage:.1f}%",
                help="7+ runs in first 5, under 9 total"
            )
        
        with col3:
            st.metric(
                label="🎲 Criteria Y",
                value=f"{y_count:,}",
                delta=f"{y_percentage:.1f}%",
                help="6+ runs in first 5, ≤9 total (excluding Criteria X)"
            )
        
        with col4:
            st.metric(
                label="✅ Total Match",
                value=f"{total_matching:,}",
                delta=f"{total_percentage:.1f}%",
                help="Combined criteria matches"
            )
        
        # Visualization
        if total_matching > 0:
            st.subheader("📈 Data Visualization")
            
            # Create pie chart
            fig_pie = go.Figure(data=[go.Pie(
                labels=['Criteria X (7+, <9)', 'Criteria Y (6+, ≤9)', 'Other Games'],
                values=[x_count, y_count, total_games - total_matching],
                hole=0.4,
                marker_colors=['#1f77b4', '#ff7f0e', '#d3d3d3']
            )])
            fig_pie.update_layout(
                title="Games Meeting Both Criteria",
                height=400
            )
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.plotly_chart(fig_pie, use_container_width=True)
            
            with col2:
                # Create comparison bar chart
                comparison_data = pd.DataFrame({
                    'Criteria': ['Criteria X\n(7+, <9)', 'Criteria Y\n(6+, ≤9)', 'Other Games'],
                    'Count': [x_count, y_count, total_games - total_matching],
                    'Percentage': [x_percentage, y_percentage, 100 - total_percentage]
                })
                
                fig_bar = px.bar(
                    comparison_data, 
                    x='Criteria', 
                    y='Count',
                    title="Criteria Comparison",
                    color='Criteria',
                    color_discrete_sequence=['#1f77b4', '#ff7f0e', '#d3d3d3']
                )
                fig_bar.update_layout(height=400, showlegend=False)
                st.plotly_chart(fig_bar, use_container_width=True)
        
        # Sample games list with tabs
        st.subheader("🎯 Sample Matching Games")
        
        if total_matching > 0:
            tab1, tab2 = st.tabs([f"🎯 Criteria X ({x_count} games)", f"🎲 Criteria Y ({y_count} games)"])
            
            with tab1:
                st.markdown("**Criteria X**: 7+ runs in first 5 innings AND under 9 total runs")
                if criteria_x_games:
                    for i, game in enumerate(criteria_x_games[:10]):
                        runs_first_5 = sum(inning['away_runs'] + inning['home_runs'] 
                                         for inning in game['innings'][:5])
                        total_runs = game['away_score'] + game['home_score']
                        
                        with st.expander(f"Game {i+1}: {game['away_team']} @ {game['home_team']} ({game['away_score']}-{game['home_score']})"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.write(f"**Date:** {game['date'][:10]}")
                                st.write(f"**Final Score:** {game['away_score']}-{game['home_score']}")
                            
                            with col2:
                                st.write(f"**First 5 Innings:** {runs_first_5} runs")
                                st.write(f"**Total Runs:** {total_runs} runs")
                            
                            with col3:
                                st.write("**✅ Meets Criteria X**")
                                st.write(f"7+ in first 5: {'✅' if runs_first_5 >= 7 else '❌'}")
                                st.write(f"Under 9 total: {'✅' if total_runs < 9 else '❌'}")
                            
                            # Inning by inning breakdown
                            inning_df = pd.DataFrame([
                                {
                                    'Inning': f"Inn {inning['inning']}",
                                    'Away': inning['away_runs'],
                                    'Home': inning['home_runs'],
                                    'Total': inning['away_runs'] + inning['home_runs']
                                }
                                for inning in game['innings']
                            ])
                            
                            st.dataframe(inning_df, use_container_width=True)
                    
                    if len(criteria_x_games) > 10:
                        st.info(f"Showing 10 of {len(criteria_x_games)} Criteria X games.")
                else:
                    st.info("No games found matching Criteria X.")
            
            with tab2:
                st.markdown("**Criteria Y**: 6+ runs in first 5 innings AND 9 or fewer total runs (excluding Criteria X)")
                if criteria_y_only:
                    for i, game in enumerate(criteria_y_only[:10]):
                        runs_first_5 = sum(inning['away_runs'] + inning['home_runs'] 
                                         for inning in game['innings'][:5])
                        total_runs = game['away_score'] + game['home_score']
                        
                        with st.expander(f"Game {i+1}: {game['away_team']} @ {game['home_team']} ({game['away_score']}-{game['home_score']})"):
                            col1, col2, col3 = st.columns(3)
                            
                            with col1:
                                st.write(f"**Date:** {game['date'][:10]}")
                                st.write(f"**Final Score:** {game['away_score']}-{game['home_score']}")
                            
                            with col2:
                                st.write(f"**First 5 Innings:** {runs_first_5} runs")
                                st.write(f"**Total Runs:** {total_runs} runs")
                            
                            with col3:
                                st.write("**✅ Meets Criteria Y**")
                                st.write(f"6+ in first 5: {'✅' if runs_first_5 >= 6 else '❌'}")
                                st.write(f"≤9 total: {'✅' if total_runs <= 9 else '❌'}")
                            
                            # Inning by inning breakdown
                            inning_df = pd.DataFrame([
                                {
                                    'Inning': f"Inn {inning['inning']}",
                                    'Away': inning['away_runs'],
                                    'Home': inning['home_runs'],
                                    'Total': inning['away_runs'] + inning['home_runs']
                                }
                                for inning in game['innings']
                            ])
                            
                            st.dataframe(inning_df, use_container_width=True)
                    
                    if len(criteria_y_only) > 10:
                        st.info(f"Showing 10 of {len(criteria_y_only)} Criteria Y games.")
                else:
                    st.info("No games found matching Criteria Y only.")
        else:
            st.info("No games found matching either criteria in the analyzed dataset.")
        
        # Download data
        if total_matching > 0:
            st.subheader("💾 Download Data")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Criteria X download
                if criteria_x_games:
                    download_data_x = []
                    for game in criteria_x_games:
                        runs_first_5 = sum(inning['away_runs'] + inning['home_runs'] 
                                         for inning in game['innings'][:5])
                        download_data_x.append({
                            'Date': game['date'][:10],
                            'Away Team': game['away_team'],
                            'Home Team': game['home_team'],
                            'Away Score': game['away_score'],
                            'Home Score': game['home_score'],
                            'First 5 Innings Runs': runs_first_5,
                            'Total Runs': game['away_score'] + game['home_score'],
                            'Criteria': 'X'
                        })
                    
                    df_download_x = pd.DataFrame(download_data_x)
                    csv_x = df_download_x.to_csv(index=False)
                    
                    st.download_button(
                        label="📥 Download Criteria X Games (CSV)",
                        data=csv_x,
                        file_name=f'mlb_{season}_criteria_x_games.csv',
                        mime='text/csv'
                    )
            
            with col2:
                # Criteria Y download
                if criteria_y_only:
                    download_data_y = []
                    for game in criteria_y_only:
                        runs_first_5 = sum(inning['away_runs'] + inning['home_runs'] 
                                         for inning in game['innings'][:5])
                        download_data_y.append({
                            'Date': game['date'][:10],
                            'Away Team': game['away_team'],
                            'Home Team': game['home_team'],
                            'Away Score': game['away_score'],
                            'Home Score': game['home_score'],
                            'First 5 Innings Runs': runs_first_5,
                            'Total Runs': game['away_score'] + game['home_score'],
                            'Criteria': 'Y'
                        })
                    
                    df_download_y = pd.DataFrame(download_data_y)
                    csv_y = df_download_y.to_csv(index=False)
                    
                    st.download_button(
                        label="📥 Download Criteria Y Games (CSV)",
                        data=csv_y,
                        file_name=f'mlb_{season}_criteria_y_games.csv',
                        mime='text/csv'
                    )
            
            # Combined download
            if criteria_x_games or criteria_y_only:
                st.markdown("---")
                all_matching = []
                
                for game in criteria_x_games:
                    runs_first_5 = sum(inning['away_runs'] + inning['home_runs'] 
                                     for inning in game['innings'][:5])
                    all_matching.append({
                        'Date': game['date'][:10],
                        'Away Team': game['away_team'],
                        'Home Team': game['home_team'],
                        'Away Score': game['away_score'],
                        'Home Score': game['home_score'],
                        'First 5 Innings Runs': runs_first_5,
                        'Total Runs': game['away_score'] + game['home_score'],
                        'Criteria': 'X'
                    })
                
                for game in criteria_y_only:
                    runs_first_5 = sum(inning['away_runs'] + inning['home_runs'] 
                                     for inning in game['innings'][:5])
                    all_matching.append({
                        'Date': game['date'][:10],
                        'Away Team': game['away_team'],
                        'Home Team': game['home_team'],
                        'Away Score': game['away_score'],
                        'Home Score': game['home_score'],
                        'First 5 Innings Runs': runs_first_5,
                        'Total Runs': game['away_score'] + game['home_score'],
                        'Criteria': 'Y'
                    })
                
                df_all = pd.DataFrame(all_matching)
                csv_all = df_all.to_csv(index=False)
                
                st.download_button(
                    label="📥 Download All Matching Games (CSV)",
                    data=csv_all,
                    file_name=f'mlb_{season}_all_criteria_games.csv',
                    mime='text/csv'
                )

    # Info section
    with st.sidebar:
        st.markdown("---")
        st.markdown("### ℹ️ About")
        st.markdown("""
        This app analyzes MLB games to find those meeting specific scoring criteria:
        
        **Criteria X:** Games with 7+ runs in the first 5 innings AND under 9 total runs for the entire game.
        
        **Criteria Y:** Games with 6+ runs in the first 5 innings AND 9 or fewer total runs (excluding Criteria X games).
        
        **Data Source:** MLB Stats API (when live data is enabled) or curated sample data.
        """)
        
        st.markdown("### 🔧 Settings")
        st.markdown("""
        - **Live Data:** Real MLB API data (slower)
        - **Sample Data:** Pre-loaded examples (faster)
        - **Days to Analyze:** More days = more accurate results
        """)

if __name__ == "__main__":
    main()
