import re

html_path = r'c:\MyResumePortfolio\blog\2026-05-20-the-enterprise-ai-model-layer-azure-model-router.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Fix Sweden Central and EU data-zone wording
html = re.sub(r'prompt and response data residency within the EU', 'prompt and response processing within the Microsoft-defined EU data zone', html, flags=re.IGNORECASE)
html = re.sub(r'High \(Supports EU Data Boundary Residency\)', 'High alignment with EU data-zone processing requirements, subject to customer legal, regulatory, and contractual validation.', html, flags=re.IGNORECASE)
html = re.sub(r'Supports EU Data Boundary Residency', 'High alignment with EU data-zone processing requirements, subject to customer legal, regulatory, and contractual validation.', html, flags=re.IGNORECASE)
html = re.sub(r'EUDB Compliant', 'High alignment with EU data-zone processing requirements, subject to customer legal, regulatory, and contractual validation.', html, flags=re.IGNORECASE)
html = re.sub(r'data remains within the EU', 'processing is aligned with the Microsoft-defined EU data zone', html, flags=re.IGNORECASE)
html = re.sub(r'guarantee data sovereignty', 'supports alignment with EU data-boundary expectations, but final sovereignty and compliance posture must still be validated against the customer’s legal, regulatory, and contractual requirements', html, flags=re.IGNORECASE)
html = re.sub(r'certified for EU Data Boundary', 'supports alignment with EU data-boundary expectations', html, flags=re.IGNORECASE)
html = re.sub(r'fully compliant', 'highly aligned with compliance frameworks', html, flags=re.IGNORECASE)

# Replace table row for Sweden Central if needed
sweden_target = r'Sweden Central.*?EU data-boundary expectations.*?(High \(Supports EU Data Boundary Residency\)|High alignment with EU data-zone processing requirements, subject to customer legal, regulatory, and contractual validation\.)'
sweden_replacement = r'Sweden Central</td><td>Strong starting point for European workloads where EU data-zone processing is required. Supports prompt and response processing within the Microsoft-defined EU data zone.</td><td>High alignment with EU data-zone processing requirements, subject to legal, regulatory, and contractual validation.'
html = re.sub(r'Sweden Central.*?EU data-boundary expectations.*?</td>\s*<td>.*?</td>', sweden_replacement + '</td>', html, flags=re.IGNORECASE | re.DOTALL)


# 2. Fix Model Router routing behavior wording
html = html.replace('Selects the cheapest model capable of execution', 'Selects a cost-effective eligible model based on routing mode, prompt complexity, and the configured model pool.')
html = html.replace('cheapest model capable', 'cost-effective eligible model')

# 3. Fix APIM / AI Gateway wording
html = html.replace('Natively runs at the edge', 'Runs as a managed API gateway layer, with tier-dependent scaling, regional deployment, policy, and observability capabilities.')

# 4. Fix safety wording
html = html.replace('Injects system safety and content filters', 'Applies prompt and response safety policies, including Azure AI Content Safety integration where configured.')

# 5. Fix "model weights" wording
html = html.replace('platform engineers tweak model weights behind the scenes', 'Model Router encapsulates this complexity by exposing a stable endpoint while platform engineers govern routing modes, eligible model subsets, and deployment policy.')

# 6. Fix FinOps calculator assumptions
html = html.replace('The default calculator value uses P = $1 per 1M input tokens only as a placeholder. Replace P with the current Model Router input-token price from Azure Pricing Calculator or your Microsoft agreement.', '')
html = re.sub(r'The calculation uses variable parameter P, which represents the input price per million tokens \(based on your Azure Enterprise Agreement or public rates\)\.', 'The default calculator value uses P = $1 per 1M input tokens only as a placeholder. Replace P with the current Model Router input-token price from Azure Pricing Calculator or your Microsoft agreement.', html)

# Replace fixed costs comparison
html = re.sub(r'Direct Premium Model \(No Router\).*?\$2,920', 'This comparison is illustrative only. Actual cost depends on current pricing, selected model, routing mode, model subset, prompt length, output length, latency, and human rework rate.', html, flags=re.IGNORECASE | re.DOTALL)
html = re.sub(r'Model Router \(Balanced Mode\).*?\$730', '', html, flags=re.IGNORECASE | re.DOTALL)
html = re.sub(r'Pilot Scale \(176 hrs\).*?\$176\.00', 'Pilot Scale (176 hrs)</td><td>Monthly cost = monthly input tokens / 1,000,000 &times; P', html, flags=re.IGNORECASE | re.DOTALL)
html = re.sub(r'Production Scale \(730 hrs\).*?\$730\.00', 'Production Scale (730 hrs)</td><td>Monthly cost = monthly input tokens / 1,000,000 &times; P', html, flags=re.IGNORECASE | re.DOTALL)


# 7. Add APIM security control table (already added in previous run, but verify and clean up)
# 8. Fix deployment checklist rendering
# Already changed to standard checkboxes, but I will ensure the 11th item is present.
if 'Configure Azure Cost Management budgets and alerts for unexpected usage shifts' not in html:
    html = html.replace('</ul>', '    <li><label><input type="checkbox"> Configure Azure Cost Management budgets and alerts for unexpected usage shifts.</label></li>\n        </ul>')


# 10. Confirm final recommendation remains strong
if 'Model Router is useful for dynamic model selection' not in html:
    html = html.replace('<p>Model Router is a Stage 2 pattern. It is a prerequisite to Stage 3, not a replacement for it.</p>', '<p>Model Router is useful for dynamic model selection, but production-grade enterprise AI still needs gateway governance, approved model subsets, observability, evaluation, FinOps controls, and human accountability.</p>\n<p>The goal is not to use the biggest model.</p>\n<p>The goal is to use the right model, for the right task, with the right controls.</p>')

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Update script v2 complete.")
