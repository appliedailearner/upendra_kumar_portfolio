import re

html_path = r'c:\MyResumePortfolio\blog\2026-05-20-the-enterprise-ai-model-layer-azure-model-router.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove unsupported savings claims
html = re.sub(r'Saves up to \d+%', 'Model Router can reduce unnecessary token spend', html, flags=re.IGNORECASE)
html = re.sub(r'up to \d+% on token expenditure', 'unnecessary token spend when simpler prompts are routed to lower-cost models while preserving higher-capability models for complex tasks. The actual saving depends on workload mix, prompt length, routing mode, selected model subset, latency, and human rework rate', html, flags=re.IGNORECASE)

metric_target = r'Evaluate cost per accepted business outcome \(factoring in latency, quality, and human rework\) instead of raw token cost\.'
metric_replacement = '''The correct enterprise metric is not raw token cost.
The better metric is cost per accepted business outcome, including token cost, latency, quality, and human correction effort.'''
html = re.sub(metric_target, metric_replacement, html, flags=re.IGNORECASE)

# 2. Remove sovereignty and compliance overclaims
html = re.sub(r'guarantees data sovereignty', 'supports alignment with EU data-boundary expectations, but final sovereignty and compliance posture must still be validated against the customer’s legal, regulatory, and contractual requirements', html, flags=re.IGNORECASE)
html = re.sub(r'EUDB Compliant', 'High alignment with EU data-zone processing requirements, subject to customer legal, regulatory, and contractual validation.', html, flags=re.IGNORECASE)
html = re.sub(r'prompt and response data remains within the EU', 'prompt and response processing is aligned with the Microsoft-defined EU data zone.', html, flags=re.IGNORECASE)
html = re.sub(r'certified for EU Data Boundary', 'supports alignment with EU data-boundary expectations', html, flags=re.IGNORECASE)
html = re.sub(r'Supports EU Data Boundary Residency', 'Supports alignment with EU data-boundary expectations', html, flags=re.IGNORECASE)


# 3. Fix region and data-boundary enforcement wording
html = html.replace('enforces region/data boundaries natively without custom API middleware', 'Model Router honors the configured deployment type and eligible model pool, including data-zone boundaries where applicable. However, enterprise enforcement still requires Azure Policy, RBAC, API gateway policy, logging, private networking, approved model governance, procurement controls, and legal review.')

# 4. Fix routing behavior wording
html = html.replace('Selects the cheapest model capable of execution', 'Selects a cost-effective eligible model based on routing mode, prompt complexity, and the configured model pool.')
html = html.replace('cheapest model capable', 'cost-effective eligible model')

# 5. Remove casual analogies
html = html.replace('Model Router (The Smart Valet)', 'Model Router: the model decision layer')
html = html.replace('AI Gateway (The Security Gate)', 'AI Gateway: the access and governance layer')

# 6. Fix APIM and safety wording
html = html.replace('Natively runs at the edge (Azure API Management)', 'Runs as a managed API gateway layer, with tier-dependent scaling, regional deployment, policy, and observability capabilities.')
html = html.replace('Natively runs at the edge', 'Runs as a managed API gateway layer, with tier-dependent scaling, regional deployment, policy, and observability capabilities.')
html = html.replace('Injects system safety and content filters', 'Applies prompt and response safety policies, including Azure AI Content Safety integration where configured.')

# 7. Replace stale model examples
html = html.replace('GPT-4o', 'higher-capability reasoning model')
html = html.replace('GPT-4o-mini', 'smaller lower-cost model')
html = html.replace('gpt-4o-0513', 'fixed model version')

# 8. Add provider caveat
# Found originally: Provider caveat: Some model families may have additional deployment requirements. For example, model families outside the default OpenAI path may need separate deployment or provider-specific setup before Model Router can route to them. Validate this during implementation instead of assuming every catalog model is immediately routable.
provider_caveat_target = r'Provider caveat: Some model families may have additional deployment requirements\. For example, model families outside the default OpenAI path may need separate deployment or provider-specific setup before Model Router can route to them\. Validate this during implementation instead of assuming every catalog model is immediately routable\.'
provider_caveat_replacement = '''Provider caveat: Some model families may have additional deployment requirements. For example, Microsoft documents that Claude models must be deployed separately before Model Router can route to them. Validate provider-specific setup before assuming every catalog model is immediately routable.'''
html = re.sub(provider_caveat_target, provider_caveat_replacement, html, flags=re.IGNORECASE)

# 9. Add version drift and auto-update risk.
drift_target = r'<h3>Version Drift and Auto-Update Risk</h3>\s*<p>.*?Model Router versions can introduce.*?human rework rate\.</p>'
drift_replacement = '''<h3>Version drift and auto-update risk</h3>
<p>Model Router versions can introduce a different set of underlying models. If auto-update is enabled, routing behavior, output quality, latency, and cost profile can change over time.</p>
<p>Production workloads should treat Model Router version updates like controlled platform changes. Evaluate the new router version against representative prompts before promotion. Track selected model, cost per workflow, latency, grounding quality, and human rework rate.</p>'''
html = re.sub(r'Version Drift and Auto-Update Risk.*?human rework rate\.', drift_replacement, html, flags=re.IGNORECASE | re.DOTALL)


# 10. Add security control table
security_table = '''
<div class="table-container">
    <table class="routing-table">
        <thead>
            <tr>
                <th>Control area</th>
                <th>Recommended control</th>
            </tr>
        </thead>
        <tbody>
            <tr><td>Identity</td><td>Use managed identity from APIM to Foundry where supported.</td></tr>
            <tr><td>Authorization</td><td>Use Entra ID, APIM products, and subscription-level access controls.</td></tr>
            <tr><td>Token governance</td><td>Use APIM token limit policy per consumer or application.</td></tr>
            <tr><td>Safety</td><td>Apply Azure AI Content Safety policies where required.</td></tr>
            <tr><td>Network exposure</td><td>Avoid direct public client access to model endpoints.</td></tr>
            <tr><td>Logging</td><td>Capture selected model, tokens, latency, caller identity, workflow ID, and outcome.</td></tr>
            <tr><td>Compliance</td><td>Use approved model subsets, data-zone-aware deployment choices, and legal review.</td></tr>
            <tr><td>Resilience</td><td>Use retry, timeout, circuit breaker, queue-based async handling, and fallback patterns.</td></tr>
        </tbody>
    </table>
</div>
'''
html = html.replace('<!-- Security Control Table Hook -->', security_table)
# if hook doesn't exist, place after AI gateway comparison
if '<!-- Security Control Table Hook -->' not in html and security_table not in html:
    html = html.replace('</ul>\n\n        <!-- Section 4: Regional Strategy -->', '</ul>\n' + security_table + '\n        <!-- Section 4: Regional Strategy -->')


# 11. Fix deployment checklist rendering
old_checklist_target = r'<div class="checklist-container">.*?All deployment readiness checks complete\. Architecture is validated\.\s*</div>\s*</div>'
new_checklist = '''
        <h2 id="deployment-checklist"><span class="gradient-text">Deployment Checklist</span></h2>
        <ul style="list-style-type: none; padding-left: 0; line-height: 1.8;">
            <li><label><input type="checkbox"> Verify the Azure AI Foundry resource is in a Model Router-supported region.</label></li>
            <li><label><input type="checkbox"> Confirm the deployment type: Global Standard or Data Zone Standard.</label></li>
            <li><label><input type="checkbox"> Validate RPM and TPM quota for the expected workload.</label></li>
            <li><label><input type="checkbox"> Define approved model subsets.</label></li>
            <li><label><input type="checkbox"> Decide whether router version auto-update is allowed.</label></li>
            <li><label><input type="checkbox"> Place the router behind APIM or another approved AI gateway where centralized governance is required.</label></li>
            <li><label><input type="checkbox"> Capture selected model, token count, latency, status code, workflow ID, and user/application identity in logs.</label></li>
            <li><label><input type="checkbox"> Define fallback behavior for throttling, timeout, and model unavailability.</label></li>
            <li><label><input type="checkbox"> Run evaluation tests before promoting to production.</label></li>
            <li><label><input type="checkbox"> Review cost, quality, latency, and human rework metrics after release.</label></li>
        </ul>
'''
html = re.sub(r'<h2 id="deployment-checklist">.*?All deployment readiness checks complete\.\s*Architecture is validated\.\s*</div>\s*</div>', new_checklist, html, flags=re.IGNORECASE | re.DOTALL)


# 12. Fix FinOps calculator and cost wording
html = html.replace('The calculation uses variable parameter P, which represents the input price per million tokens (based on your Azure Enterprise Agreement or public rates).', 'The default calculator value uses P = $1 per 1M input tokens only as a placeholder. Replace P with the current Model Router input-token price from Azure Pricing Calculator or your Microsoft agreement.')
html = html.replace('Monthly cost = Hourly cost &times; active usage hours per month', 'Monthly cost = monthly input tokens / 1,000,000 &times; P')
html = html.replace('Monthly cost = Hourly cost × active usage hours per month', 'Monthly cost = monthly input tokens / 1,000,000 × P')

html = html.replace('<!-- Finops cost sentence -->', '<p>A low-cost model output that needs human rework is not cheap. A higher-cost model that produces a trusted answer in one pass may be cheaper at the workflow level.</p>')
if 'A low-cost model output that needs human rework is not cheap.' not in html:
    html = re.sub(r'(<h2 id="finops-calculator">.*?)(<div class="finops-calculator">)', r'\1<p>A low-cost model output that needs human rework is not cheap. A higher-cost model that produces a trusted answer in one pass may be cheaper at the workflow level.</p>\n\2', html, flags=re.IGNORECASE | re.DOTALL)


# 13. Improve region wording
region_target = r'As of the Microsoft documentation reviewed on 20 May 2026, Model Router deployment requires the Azure AI Foundry resource to be in:'
region_replacement = 'As of the current Microsoft documentation, Model Router deployment requires the Foundry resource to be in East US 2 or Sweden Central. This should be validated before production rollout because Azure AI Foundry feature availability can vary by model, deployment type, quota, and region.'
html = html.replace(region_target, region_replacement)
html = re.sub(r'As of the current Microsoft documentation, Model Router deployment requires the Azure AI Foundry resource to be in East US 2 or Sweden Central\..*?and region\.', region_replacement, html, flags=re.DOTALL)


# 14. Add production failure section
failure_section = '''
        <h2 id="production-failures"><span class="gradient-text">What Can Go Wrong in Production</span></h2>
        <p>Model routing can fail as an operating model if teams do not control the surrounding platform.</p>
        <p>Common failure patterns include:</p>
        <ul>
            <li>Treating Model Router as a full AI governance layer.</li>
            <li>Allowing uncontrolled model subsets in production.</li>
            <li>Ignoring router version changes and auto-update behavior.</li>
            <li>Measuring only token cost instead of cost per accepted outcome.</li>
            <li>Sending large documents directly to the model instead of using extraction, chunking, retrieval, and grounding.</li>
            <li>Using dynamic routing for regulated workflows that require a fixed approved model.</li>
            <li>Failing to log the selected model, token usage, latency, caller identity, and workflow context.</li>
            <li>Assuming data-zone alignment equals complete legal sovereignty.</li>
        </ul>
        <p>The fix is not to avoid Model Router. The fix is to use it inside a governed AI platform with gateway controls, approved model subsets, observability, evaluation, FinOps controls, and human accountability.</p>
'''
# Replace the old 'What Can Go Wrong in Production' section
html = re.sub(r'<h2 id="what-can-go-wrong">.*?The fix is not to avoid Model Router.*?that is the real risk\.\s*</p>', failure_section, html, flags=re.IGNORECASE | re.DOTALL)


# 15. Strengthen final recommendation
recommendation_end = '''Model Router is useful for dynamic model selection, but production-grade enterprise AI still needs gateway governance, approved model subsets, observability, evaluation, FinOps controls, and human accountability.</p>
<p>The goal is not to use the biggest model.</p>
<p>The goal is to use the right model, for the right task, with the right controls.</p>'''
html = re.sub(r'Model Router is a Stage 2 pattern\. It is a prerequisite to Stage 3, not a replacement for it\.\s*</p>', recommendation_end, html, flags=re.IGNORECASE)

# 16. Remove UTM tracking from links
html = re.sub(r'\?utm_source=chatgpt\.com(&[^"]*)?', '', html, flags=re.IGNORECASE)
html = re.sub(r'&utm_source=chatgpt\.com(&[^"]*)?', '', html, flags=re.IGNORECASE)


with open(html_path, 'w', encoding='utf-8') as f:
    f.write(html)
print("Finished update script")
