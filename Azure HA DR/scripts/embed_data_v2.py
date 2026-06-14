import json
import os

html_path = r'c:\MyResumePortfolio\Azure HA DR\index.html'
json_path = r'c:\MyResumePortfolio\Azure HA DR\compact_data.json'

with open(html_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(json_path, 'r', encoding='utf-8') as f:
    data_str = f.read()

# I'll replace everything between 'async function loadData() {' and 'function getUniqueValues'
# By searching for line patterns

new_lines = []
skip = False
for line in lines:
    if 'async function loadData() {' in line:
        new_lines.append('            async function loadData() {\n')
        new_lines.append('                try {\n')
        new_lines.append('                    const dataElem = document.getElementById("decision-matrix-data");\n')
        new_lines.append('                    if (dataElem) {\n')
        new_lines.append('                        const raw = JSON.parse(dataElem.textContent);\n')
        new_lines.append('                        const headers = raw.headers;\n')
        new_lines.append('                        decisionMatrix = raw.rows.map(row => {\n')
        new_lines.append('                            const obj = {};\n')
        new_lines.append('                            headers.forEach((h, i) => { obj[h] = row[i]; });\n')
        new_lines.append('                            return obj;\n')
        new_lines.append('                        });\n')
        new_lines.append('                        console.log("Decision matrix data loaded from embedded JSON:", decisionMatrix.length, "rows");\n')
        new_lines.append('                        initializeInputOptions();\n')
        new_lines.append('                    } else {\n')
        new_lines.append('                        throw new Error("Embedded data script not found");\n')
        new_lines.append('                    }\n')
        new_lines.append('                } catch (err) {\n')
        new_lines.append('                    console.error("Data load error:", err);\n')
        new_lines.append('                    showErrorBanner("Could not load the embedded decision matrix. Error: " + err.message);\n')
        new_lines.append('                }\n')
        new_lines.append('            }\n')
        skip = True
    elif 'function getUniqueValues' in line and skip:
        new_lines.append('\n')
        new_lines.append(line)
        skip = False
    elif not skip:
        # Also handle the script tag injection
        if '</body>' in line:
            new_lines.append(f'<script id="decision-matrix-data" type="application/json">{data_str}</script>\n')
            new_lines.append(line)
        elif '<script src="data/decision_data.js"></script>' in line:
            continue
        else:
            new_lines.append(line)

with open(html_path, 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print("Embedded successfully.")
