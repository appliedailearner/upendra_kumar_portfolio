import logging
import azure.functions as func
import time
import json
import os
import urllib.request
import urllib.error

def main(req: func.HttpRequest) -> func.HttpResponse:
    start = time.time()
    # Pinging a reliable target (e.g. Azure Home)
    target_url = os.environ.get('TARGET_STORAGE_URL', 'https://azure.microsoft.com/en-in/')
    
    try:
        # Use urllib instead of requests to avoid dependency issues
        req = urllib.request.Request(
            target_url, 
            method='HEAD',
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        
        with urllib.request.urlopen(req, timeout=5) as response:
            pass # Just need the headers/status
            
        latency = (time.time() - start) * 1000 # to ms
        
        return func.HttpResponse(
            json.dumps({
                "region": "Central India",
                "latency_ms": int(latency),
                "status": "Online"
            }),
            mimetype="application/json",
            headers={
                'Access-Control-Allow-Origin': '*'
            }
        )
    except Exception as e:
        logging.error(f"Latency probe error: {str(e)}")
        return func.HttpResponse(
            json.dumps({
                "region": "Central India", 
                "latency_ms": 0,
                "status": "Offline",
                "error": str(e)
            }),
            status_code=200, # Return 200 so frontend can parse the "Offline" status cleanly
            mimetype="application/json",
            headers={
                'Access-Control-Allow-Origin': '*'
            }
        )
