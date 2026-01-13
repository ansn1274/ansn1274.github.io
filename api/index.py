from fastapi import FastAPI, HTTPException
from nba_api.stats.static import players
from nba_api.stats.endpoints import shotchartdetail, playercareerstats
import pandas as pd

app = FastAPI()

@app.get("/api/test")
def test():
    return {"message": "NBA API is LIVE via FastAPI (api/index.py)"}

@app.get("/api/search_players")
def search_players(name: str = None):
    if not name:
        return []
    
    nba_players = players.get_players()
    results = [
        {
            "id": p["id"],
            "full_name": p["full_name"],
            "is_active": p["is_active"]
        }
        for p in nba_players 
        if name.lower() in p["full_name"].lower()
    ]
    
    return results[:10]

@app.get("/api/player_stats")
def get_player_stats(player_id: str, season: str = "2023-24"):
    try:
        # 1. Get Shot Chart Data
        sc = shotchartdetail.ShotChartDetail(
            player_id=player_id,
            team_id=0,
            season_nullable=season,
            context_measure_simple='FGA'
        )
        shot_df = sc.get_data_frames()[0]
        
        # 2. Get Career/Season Stats
        career = playercareerstats.PlayerCareerStats(player_id=player_id)
        stats_df = career.get_data_frames()[0]
        
        # Format results
        shots_list = []
        if not shot_df.empty:
            shots_list = shot_df[['LOC_X', 'LOC_Y', 'EVENT_TYPE', 'SHOT_TYPE', 'SHOT_DISTANCE', 'SHOT_MADE_FLAG']].to_dict(orient='records')
        
        stats_list = []
        if not stats_df.empty:
            stats_list = stats_df.to_dict(orient='records')

        return {
            "shots": shots_list,
            "stats": stats_list
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
