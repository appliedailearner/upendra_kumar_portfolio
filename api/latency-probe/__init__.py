import logging
import azure.functions as func
import time
import json
import os
import requests

def main(req: func.HttpRequest) -> func.HttpResponse:
    start = time.time()
    # Pinging a reliable target (e.g. Azure Home or the storage account if env var set)
    target_url = os.environ.get('TARGET_STORAGE_URL', 'https://azure.microsoft.com/en-in/')
    
    try:
        response = requests.head(target_url, timeout=5)
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
        return func.HttpResponse(
            "Error pinging target",
            status_code=500
        )
