from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
from nba_api.stats.static import players

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        query = parse_qs(urlparse(self.path).query)
        name = query.get('name', [None])[0]
        
        if not name:
            self.send_response(400)
            self.end_headers()
            return
            
        # Search for players
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
        
        # Limit to top 10 results
        results = results[:10]
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(results).encode('utf-8'))
        return
