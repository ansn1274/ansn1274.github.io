import os
from urllib.parse import urlencode, quote_plus
from requests.sessions import Session

def apply_scraperapi_proxy():
    """
    Checks for SCRAPER_API_KEY environment variable. 
    If present, monkeypatches requests.Session.request to route traffic 
    through ScraperAPI's endpoint mode.
    """
    scraper_key = os.environ.get('SCRAPER_API_KEY')
    
    if not scraper_key:
        return

    # Store original request method to avoid recursion loops if called multiple times
    if getattr(Session.request, '_is_monkeypatched', False):
        return

    original_request = Session.request
    
    def scraperapi_request(self, method, url, *args, **kwargs):
        # 1. Reconstruct full URL with params if they exist
        params = kwargs.get('params')
        if params:
            url_sep = '&' if '?' in url else '?'
            url += url_sep + urlencode(params)
            kwargs['params'] = None
            
        # 2. Wrap with ScraperAPI URL
        # Format: http://api.scraperapi.com?api_key=KEY&url=ENCODED_TARGET_URL
        target_url = quote_plus(url)
        scraper_url = f"http://api.scraperapi.com?api_key={scraper_key}&url={target_url}"
        
        # 3. Clean up kwargs
        if 'proxies' in kwargs:
            kwargs.pop('proxies')
            
        # 4. Append keep_headers=true to ensure NBA.com sees our custom headers
        scraper_url += "&keep_headers=true"
        
        # Note: headers in kwargs are passed through to ScraperAPI -> Target
        
        return original_request(self, method, scraper_url, *args, **kwargs)
    
    # Mark as patched
    scraperapi_request._is_monkeypatched = True
    Session.request = scraperapi_request
