from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from nba_api.stats.endpoints import shotchartdetail, playercareerstats
import pandas as pd

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        player_id = query.get('player_id', [None])[0]
        season = query.get('season', ["2023-24"])[0]
        
        if not player_id:
            self.send_response(400)
            self.end_headers()
            return
            
        try:
            # 1. Get Shot Chart Data
            # Note: team_id=0 for all teams
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
            data = {
                "shots": shot_df[['LOC_X', 'LOC_Y', 'EVENT_TYPE', 'SHOT_TYPE', 'SHOT_DISTANCE', 'SHOT_MADE_FLAG']].to_dict(orient='records'),
                "stats": stats_df.to_dict(orient='records')
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(data).encode('utf-8'))
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
            
        return
