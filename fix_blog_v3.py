import re

with open(r"c:\MyResumePortfolio\blog_445826f.html", "r", encoding="utf-16") as f:
    content = f.read()

# 1. Fix fonts
font_import = """    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@700;800;900&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">"""
if "fonts.googleapis.com" not in content:
    content = content.replace("</head>", f"{font_import}\n</head>")

# 2. Fix titles
content = re.sub(r'<title>.*?</title>', '<title>Azure Model Router: The Enterprise AI Model Layer | Upendra Kumar</title>', content)
content = re.sub(r'<h1 class="hero-title">.*?</h1>', '<h1 class="hero-title">\n                Azure Model Router: The Enterprise AI Model Layer\n            </h1>', content, flags=re.DOTALL)

# 3. Enhance Workload Mapping Table to Glass Cards
old_table = """<div style="overflow-x: auto; overflow-y: hidden;">
            <table class="styled-table" style="min-width: 600px;">
                <thead>
                    <tr>
                        <th>Task Type</th>
                        <th>Complexity</th>
                        <th>Ideal Model Tier</th>
                        <th>Model Router Routing Mode</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Support Ticket Triage</td>
                        <td>Low</td>
                        <td>Cheaper (smaller lower-cost model)</td>
                        <td>Cost Mode</td>
                    </tr>
                    <tr>
                        <td>FAQ Response Drafting</td>
                        <td>Low</td>
                        <td>Cheaper (smaller lower-cost model)</td>
                        <td>Cost Mode</td>
                    </tr>
                    <tr>
                        <td>Customer Sentiment Analysis</td>
                        <td>Medium</td>
                        <td>Cheaper (smaller lower-cost model)</td>
                        <td>Balanced Mode</td>
                    </tr>
                    <tr>
                        <td>Comprehensive Document Summarization</td>
                        <td>Medium</td>
                        <td>Balanced Selection</td>
                        <td>Balanced Mode</td>
                    </tr>
                    <tr>
                        <td>Contract Risk & Compliance Auditing</td>
                        <td>High</td>
                        <td>Advanced (higher-capability reasoning model)</td>
                        <td>Quality Mode / Fixed Pinning</td>
                    </tr>
                    <tr>
                        <td>SQL Code Generation</td>
                        <td>High</td>
                        <td>Advanced / Specialized</td>
                        <td>Quality Mode / Fixed Pinning</td>
                    </tr>
                </tbody>
            </table>
        </div>"""

new_cards = """<div class="responsive-grid" style="gap: 1.5rem; margin-top: 2rem;">
            <!-- Low Complexity -->
            <div class="glass-card reveal reveal-delay-1" style="border-top: 4px solid #34d399;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <span class="badge-router-cost" style="padding: 0.25rem 0.75rem; border-radius: 99px; font-size: 0.8rem; font-weight: 600; background: rgba(52, 211, 153, 0.15); color: #34d399; border: 1px solid rgba(52, 211, 153, 0.3);">Cost Mode</span>
                    <span style="color: #94a3b8; font-size: 0.85rem;"><i class="fas fa-arrow-down"></i> Low Complexity</span>
                </div>
                <h3 style="color: #f8fafc; margin-top: 0; font-size: 1.1rem;">Support Triage & FAQ Drafting</h3>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 0;">Routes to smaller, lower-cost models optimized for high-volume, repetitive text generation.</p>
            </div>

            <!-- Medium Complexity -->
            <div class="glass-card reveal reveal-delay-2" style="border-top: 4px solid #60a5fa;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <span class="badge-router-balanced" style="padding: 0.25rem 0.75rem; border-radius: 99px; font-size: 0.8rem; font-weight: 600; background: rgba(96, 165, 250, 0.15); color: #60a5fa; border: 1px solid rgba(96, 165, 250, 0.3);">Balanced Mode</span>
                    <span style="color: #94a3b8; font-size: 0.85rem;"><i class="fas fa-exchange-alt"></i> Medium Complexity</span>
                </div>
                <h3 style="color: #f8fafc; margin-top: 0; font-size: 1.1rem;">Sentiment Analysis & Summarization</h3>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 0;">Balanced selection across eligible tiers for moderate reasoning tasks requiring nuanced understanding.</p>
            </div>

            <!-- High Complexity -->
            <div class="glass-card reveal reveal-delay-3" style="border-top: 4px solid #a855f7;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 1rem;">
                    <span class="badge-router-quality" style="padding: 0.25rem 0.75rem; border-radius: 99px; font-size: 0.8rem; font-weight: 600; background: rgba(168, 85, 247, 0.15); color: #a855f7; border: 1px solid rgba(168, 85, 247, 0.3);">Quality Mode / Fixed</span>
                    <span style="color: #94a3b8; font-size: 0.85rem;"><i class="fas fa-arrow-up"></i> High Complexity</span>
                </div>
                <h3 style="color: #f8fafc; margin-top: 0; font-size: 1.1rem;">Risk Audits & SQL Generation</h3>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 0;">Routes strictly to advanced reasoning capabilities or specialized endpoints where accuracy is paramount.</p>
            </div>
        </div>"""

if old_table in content:
    content = content.replace(old_table, new_cards)
else:
    print("Warning: old table not found for replacement.")


# 4. Enhance the routing mode table to use glass-card styles
old_routing_table = """<div style="overflow-x: auto; overflow-y: hidden;">
            <table class="styled-table" style="min-width: 600px;">
                <thead>
                    <tr>
                        <th>Routing Mode</th>
                        <th>What it Optimizes For</th>
                        <th>Best Fit Workloads</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td><strong>Balanced</strong></td>
                        <td>Best combination of quality and cost</td>
                        <td>Default enterprise workloads and interactive assistants</td>
                    </tr>
                    <tr>
                        <td><strong>Cost</strong></td>
                        <td>Lower-cost model selection (e.g. smaller lower-cost model)</td>
                        <td>High-volume, lower-risk classification/extraction tasks</td>
                    </tr>
                    <tr>
                        <td><strong>Quality</strong></td>
                        <td>Highest-quality response (e.g. higher-capability reasoning model)</td>
                        <td>Complex multi-step reasoning and critical regulatory tasks</td>
                    </tr>
                </tbody>
            </table>
        </div>"""

new_routing_cards = """<div class="responsive-grid" style="margin-bottom: 2rem;">
            <div class="glass-card reveal" style="padding: 1.5rem; background: linear-gradient(145deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));">
                <h4 style="color: #60a5fa; margin-top: 0; font-size: 1.1rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;"><i class="fas fa-balance-scale"></i> Balanced Mode</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 0.5rem;"><strong>Optimizes:</strong> Best combination of quality and cost.</p>
                <p style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0;"><strong>Fit:</strong> Default enterprise workloads and interactive assistants.</p>
            </div>
            <div class="glass-card reveal reveal-delay-1" style="padding: 1.5rem; background: linear-gradient(145deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));">
                <h4 style="color: #34d399; margin-top: 0; font-size: 1.1rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;"><i class="fas fa-coins"></i> Cost Mode</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 0.5rem;"><strong>Optimizes:</strong> Lower-cost model selection.</p>
                <p style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0;"><strong>Fit:</strong> High-volume, lower-risk classification/extraction.</p>
            </div>
            <div class="glass-card reveal reveal-delay-2" style="padding: 1.5rem; background: linear-gradient(145deg, rgba(30, 41, 59, 0.7), rgba(15, 23, 42, 0.8));">
                <h4 style="color: #a855f7; margin-top: 0; font-size: 1.1rem; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 0.5rem;"><i class="fas fa-gem"></i> Quality Mode</h4>
                <p style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 0.5rem;"><strong>Optimizes:</strong> Highest-quality reasoning output.</p>
                <p style="font-size: 0.9rem; color: #94a3b8; margin-bottom: 0;"><strong>Fit:</strong> Complex multi-step reasoning, critical regulatory tasks.</p>
            </div>
        </div>"""
if old_routing_table in content:
    content = content.replace(old_routing_table, new_routing_cards)
else:
    print("Warning: old routing table not found for replacement.")


# 5. Fix FinOps disclaimer
disclaimer = """<div class="callout-box" style="margin-top: 2rem; background: rgba(59, 130, 246, 0.1); border-left: 4px solid #3b82f6;">
            <h4><i class="fas fa-info-circle"></i> Cost Estimation Disclaimer</h4>
            This comparison is illustrative only. Actual cost depends on current pricing, selected model, routing mode, model subset, prompt length, output length, latency, and human rework rate.
        </div>"""

if disclaimer not in content:
    content = content.replace('<!-- Table Lookup View (Hidden by default) -->', f"{disclaimer}\n\n        <!-- Table Lookup View (Hidden by default) -->")

with open(r"c:\MyResumePortfolio\blog\2026-05-20-the-enterprise-ai-model-layer-azure-model-router.html", "w", encoding="utf-8") as f:
    f.write(content)

print("HTML transformations applied successfully.")
