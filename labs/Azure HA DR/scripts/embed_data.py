import json
import os
import re

html_path = r'c:\MyResumePortfolio\Azure HA DR\index.html'
json_path = r'c:\MyResumePortfolio\Azure HA DR\compact_data.json'

with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# Find any existing or new script tags for data and remove
html = re.sub(r'<script src="data/decision_data.js"></script>', '', html)
html = re.sub(r'<script id="decision-matrix-data".*?</script>', '', html, flags=re.DOTALL)

# Prepare the embedded data script
embedded_data_script = f'<script id="decision-matrix-data" type="application/json">{json.dumps(data)}</script>'

# Inject before the first closing </body> tag
html = html.replace('</body>', embedded_data_script + '\n</body>')

# Update loadData to read from this tag
new_load_data_body = """
                try {
                    const dataElem = document.getElementById('decision-matrix-data');
                    if (dataElem) {
                        const raw = JSON.parse(dataElem.textContent);
                        const headers = raw.headers;
                        decisionMatrix = raw.rows.map(row => {
                            const obj = {};
                            headers.forEach((h, i) => { obj[h] = row[i]; });
                            return obj;
                        });
                        console.log('Decision matrix data loaded from embedded JSON:', decisionMatrix.length, 'rows');
                        initializeInputOptions();
                    } else {
                        throw new Error('Embedded data script not found');
                    }
                } catch (err) {
                    console.error('Data load error:', err);
                    showErrorBanner('Could not load the embedded decision matrix. Error: ' + err.message);
                }
"""

# Replace the loadData function body
# This regex targets the loadData function body until the next function
html = re.sub(r'async function loadData\(\) \{.*?\}\n\n            function getUniqueValues', 
              f'async function loadData() {{{new_load_data_body}\n            }}\n\n            function getUniqueValues', 
              html, flags=re.DOTALL)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)

print("Success: Data embedded and loadData refactored.")
