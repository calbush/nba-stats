from flask import Flask, render_template
from nba_api.stats.endpoints import playercareerstats, commonplayerinfo
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('build/index.html')

@app.route('/players/<player_id>')
def get_player(player_id):
    player = commonplayerinfo.CommonPlayerInfo(player_id=player_id)
    info = player.get_data_frames()[0]

    career = playercareerstats.PlayerCareerStats(player_id=player_id)
    stats = career.get_data_frames()[0] #Player stats dataframe

    career_seasons_played = len(stats['SEASON_ID'])
    current_season = stats['SEASON_ID'].max()
    current_season_stats = stats[stats['SEASON_ID'] == current_season]

    career_totals = stats.groupby('SEASON_ID')[['GP', 'PTS', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'FG_PCT', 'FG3_PCT', 'FTA', 'FT_PCT']].sum()
    

    Player = {
        'info': {
            'name': info['DISPLAY_FI_LAST'].iloc[0],
            'height': info['HEIGHT'].iloc[0],
            'weight': info['WEIGHT'].iloc[0],
            'position': info['POSITION'].iloc[0],
            'number': info['JERSEY'].iloc[0],
            'team': info['TEAM_NAME'].iloc[0],
            'id': player_id
        },
        'career_averages': {
            'PPG': round(career_totals['PTS'].sum() / career_totals['GP'].sum(), 1),
            'RPG': round(career_totals['REB'].sum() / career_totals['GP'].sum(), 1),
            'APG': round(career_totals['AST'].sum() / career_totals['GP'].sum(), 1),
            'SPG': round(career_totals['STL'].sum() / career_totals['GP'].sum(), 1),
            'BPG': round(career_totals['BLK'].sum() / career_totals['GP'].sum(), 1),
            'TOV': round(career_totals['TOV'].sum() / career_totals['GP'].sum(), 1),
            'FTA': round(career_totals['FTA'].sum() / career_totals['GP'].sum(), 1),
            'FG_PCT': round(career_totals['FG_PCT'].sum() / career_seasons_played, 3) * 100,
            'FG3_PCT': round(career_totals['FG3_PCT'].sum() / career_seasons_played, 3) * 100,
            'FT_PCT': round(career_totals['FT_PCT'].sum() / career_seasons_played, 3) * 100,
        },
        'current_season_averages': {
            'PPG': round(current_season_stats['PTS'].iloc[0] / current_season_stats['GP'].iloc[0], 1),
            'RPG': round(current_season_stats['REB'].iloc[0] / current_season_stats['GP'].iloc[0], 1),
            'APG': round(current_season_stats['AST'].iloc[0] / current_season_stats['GP'].iloc[0], 1),
            'SPG': round(current_season_stats['STL'].iloc[0] / current_season_stats['GP'].iloc[0], 1),
            'BPG': round(current_season_stats['BLK'].iloc[0] / current_season_stats['GP'].iloc[0], 1),
            'TOV': round(current_season_stats['TOV'].iloc[0] / current_season_stats['GP'].iloc[0], 1),
            'FTA': round(current_season_stats['FTA'].iloc[0] / current_season_stats['GP'].iloc[0], 1),
            'FG_PCT': current_season_stats['FG_PCT'].iloc[0] * 100,
            'FG3_PCT': current_season_stats['FG3_PCT'].iloc[0] * 100,
            'FT_PCT': current_season_stats['FT_PCT'].iloc[0] * 100,
        }
    }

    print(Player)

    return Player

