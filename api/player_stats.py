from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
from nba_api.stats.endpoints import playercareerstats, shotchartdetail

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        player_id = query_params.get('player_id', [None])[0]
        season = query_params.get('season', ['2023-24'])[0]

        if not player_id:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": "Missing player_id"}).encode())
            return

        try:
            # 1. Fetch Shot Chart Data
            # Note: ContextMeasure='FGA' is common for all attempts
            scd = shotchartdetail.ShotChartDetail(
                player_id=player_id,
                team_id=0,
                season_nullable=season,
                context_measure_simple='FGA'
            )
            shots_df = scd.get_data_frames()[0]
            shots = shots_df[['LOC_X', 'LOC_Y', 'EVENT_TYPE', 'SHOT_MADE_FLAG']].to_dict(orient='records')

            # 2. Fetch Career Stats
            career = playercareerstats.PlayerCareerStats(player_id=player_id)
            stats_df = career.get_data_frames()[0]
            stats = stats_df[['SEASON_ID', 'PTS', 'REB', 'AST', 'TEAM_ABBREVIATION']].to_dict(orient='records')

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps({"shots": shots, "stats": stats}).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
