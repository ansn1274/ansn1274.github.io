from http.server import BaseHTTPRequestHandler
import json
from urllib.parse import parse_qs, urlparse
from nba_api.stats.static import players

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed_path = urlparse(self.path)
        query_params = parse_qs(parsed_path.query)
        
        name = query_params.get('name', [None])[0]

        if not name:
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps([]).encode())
            return

        try:
            # Fetch all players
            all_players = players.get_players()
            
            # Filter by name (simple case-insensitive contains)
            filtered = [
                {
                    "id": p["id"],
                    "full_name": p["full_name"],
                    "is_active": p["is_active"]
                }
                for p in all_players
                if name.lower() in p["full_name"].lower()
            ]
            
            # Limit results
            filtered = filtered[:10]

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(filtered).encode())
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({"error": str(e)}).encode())
