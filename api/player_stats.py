from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import parse_qs, urlparse
from nba_api.stats.endpoints import playercareerstats, shotchartdetail
from api.utils import apply_scraperapi_proxy

# Apply Proxy logic if on Vercel Production
apply_scraperapi_proxy()

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
            custom_headers = {
                'Accept': 'application/json, text/plain, */*',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
                'Referer': 'https://stats.nba.com/',
                'Accept-Encoding': 'gzip, deflate, br',
                'Accept-Language': 'en-US,en;q=0.9',
            }
            # Set to 50 seconds to give ScraperAPI time (Vercel max is usually 60s)
            timeout_val = 50
            
            # Note: We rely on the monkeypatch above to handle the proxying if scraper_key is present.
            # We do NOT pass proxy_config explicitly to nba_api anymore because the patch handles the URL rewriting.

            # 1. Fetch Shot Chart Data
            # Note: ContextMeasure='FGA' is common for all attempts
            scd = shotchartdetail.ShotChartDetail(
                player_id=player_id,
                team_id=0,
                season_nullable=season,
                context_measure_simple='FGA',
                headers=custom_headers,
                timeout=timeout_val
            )
            shots_df = scd.get_data_frames()[0]
            shots = shots_df[['LOC_X', 'LOC_Y', 'EVENT_TYPE', 'SHOT_MADE_FLAG']].to_dict(orient='records')

            # 2. Fetch Career Stats
            career = playercareerstats.PlayerCareerStats(
                player_id=player_id,
                headers=custom_headers,
                timeout=timeout_val
            )
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
