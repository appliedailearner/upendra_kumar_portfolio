# 🚨 Azure Function Deployment Fix

The automated deployment for the Azure Function `func-portfolio-latency-py` appears to have stalled or completed without successfully syncing the code. The resource exists, but the endpoint returns `404 Not Found`.

## Steps to Fix Manually

1.  **Open Terminal** in your project root.
2.  **Navigate directly to the API folder**:
    ```powershell
    cd api/latency-probe
    ```
    *(Note: Ensure you are in the folder containing `host.json` or `local.settings.json`. If `api` is the root of the function app, go there.)*

3.  **Run the Publish Command**:
    ```powershell
    func azure functionapp publish func-portfolio-latency-py
    ```
    *(If prompted to select language, choose **Node.js** or **JavaScript** based on your local code).*

4.  **Verify**:
    Once the command finishes successfully, visit:
    [https://func-portfolio-latency-py.azurewebsites.net/api/latency-probe](https://func-portfolio-latency-py.azurewebsites.net/api/latency-probe)

    You should see a JSON response:
    ```json
    {"region": "...", "latency_ms": ...}
    ```


5.  **Frontend Update**:
    The `index.html` is already configured to point to this URL. Once the backend is fixed, the widget on your portfolio will automatically start working.

## ⚠️ Troubleshooting "500 Internal Server Error"

If you see a `500` error, it means the Python code is crashing on startup. This is likely due to missing dependencies.

1.  **Check Logs in Portal**:
    *   Go to [Azure Portal](https://portal.azure.com).
    *   Navigate to Function App: `func-portfolio-latency-py`.
    *   Click **"Log Stream"** in the left menu.
    *   Refresh the API URL. The error will appear in the logs.

2.  **Verify Requirements**:
    Ensure `requirements.txt` is in the root of your deployment package and contains:
    ```text
    azure-functions
    requests
    ```


### Only if the above fails (Persistent 500 Error):

If `func publish` succeeds but the endpoint still returns 500 (even with Hello World code), the **Function App Resource itself is likely corrupted** (e.g., Python version mismatch or storage link broken).

**Solution:**
1.  Go to Azure Portal.
2.  **Delete** `func-portfolio-latency-py`.
### Solution (Final):
1.  **Node.js Migration**: The backend has been migrated to Node.js (v20) to resolve Python runtime issues.
2.  **New Endpoint**: `https://func-portfolio-latency-node-7433.azurewebsites.net/api/latency-probe`
3.  **No Action Required**: The `index.html` has been updated to use this new, stable endpoint.
4.  **Verification**: Refresh the page to see live latency (calculated client-side).




