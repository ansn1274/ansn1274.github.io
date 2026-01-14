from http.server import HTTPServer, BaseHTTPRequestHandler
import sys
import os

# Add local directory to path ensuring imports work
sys.path.append(os.path.dirname(__file__))

# Import handlers
try:
    from api.search_players import handler as SearchHandler
    from api.player_stats import handler as StatsHandler
    from api.index import handler as IndexHandler
except ImportError as e:
    print(f"Error importing handlers: {e}")
    sys.exit(1)

class Router(BaseHTTPRequestHandler):
    def do_GET(self):
        # Route requests to the appropriate handler
        # We manually invoke the do_GET method of the Vercel handler classes,
        # passing 'self' so they can write to the response stream.
        try:
            if self.path.startswith('/api/search_players'):
                SearchHandler.do_GET(self)
            elif self.path.startswith('/api/player_stats'):
                StatsHandler.do_GET(self)
            elif self.path.startswith('/api'):
                # Default/Fallback to index
                IndexHandler.do_GET(self)
            else:
                self.send_error(404, "Endpoint not found in dev server")
        except Exception as e:
            self.send_error(500, f"Internal Server Error: {str(e)}")

def run(server_class=HTTPServer, handler_class=Router, port=8300):
    server_address = ('127.0.0.1', port)
    httpd = server_class(server_address, handler_class)
    print(f"🏀 Python BFF Dev Server running on http://127.0.0.1:{port}")
    print(f"   - /api/search_players")
    print(f"   - /api/player_stats")
    print(f"Press CTRL+C to stop")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print("Server stopped.")

if __name__ == "__main__":
    run()
