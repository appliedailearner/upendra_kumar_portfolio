import os

template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Presentation - {title}</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css">
    <style>
        :root {{
            --bg-dark: #0f172a;
            --card-bg: #1e293b;
            --text-primary: #f8fafc;
            --text-secondary: #94a3b8;
            --accent: #38bdf8;
            --border: #334155;
        }}
        body {{ 
            background-color: var(--bg-dark); 
            color: var(--text-primary); 
            font-family: 'Inter', -apple-system, sans-serif; 
            padding: 2rem 0;
            line-height: 1.6;
        }}
        .container {{ max-width: 900px; }}
        .slide {{ 
            background: var(--card-bg); 
            border-radius: 16px; 
            padding: 4rem; 
            margin-bottom: 3rem; 
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.2); 
            border: 1px solid var(--border);
            position: relative;
            overflow: hidden;
        }}
        .slide::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: var(--accent);
        }}
        h1 {{ color: var(--accent); font-weight: 800; margin-bottom: 1.5rem; font-size: 2.5rem; }}
        h2 {{ color: var(--text-secondary); font-weight: 600; margin-bottom: 2rem; font-size: 1.5rem; }}
        h3 {{ color: var(--accent); font-size: 1.25rem; margin-top: 2rem; margin-bottom: 1rem; text-transform: uppercase; letter-spacing: 0.05em; }}
        ul {{ list-style-type: none; padding-left: 0; }}
        li {{ margin-bottom: 1rem; position: relative; padding-left: 1.5rem; }}
        li::before {{
            content: '→';
            position: absolute;
            left: 0;
            color: var(--accent);
        }}
        .footer {{ 
            font-size: 0.85rem; 
            color: #64748b; 
            margin-top: 3rem; 
            padding-top: 1.5rem;
            border-top: 1px solid var(--border);
            display: flex;
            justify-content: space-between;
        }}
        img {{ 
            max-width: 100%; 
            border-radius: 12px; 
            margin-top: 2rem; 
            border: 1px solid var(--border);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
        }}
        .btn-back {{ 
            margin-bottom: 3rem; 
            color: var(--accent); 
            text-decoration: none; 
            display: inline-flex; 
            align-items: center;
            font-weight: 600;
            transition: all 0.2s;
        }}
        .btn-back:hover {{ transform: translateX(-5px); color: #7dd3fc; }}
        .btn-back i {{ margin-right: 0.5rem; }}
        .badge-tech {{
            background: rgba(56, 189, 248, 0.1);
            color: var(--accent);
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.8rem;
            font-weight: 600;
            border: 1px solid rgba(56, 189, 248, 0.2);
        }}
        strong {{ color: var(--accent); }}
    </style>
</head>
<body>
    <div class="container">
        <a href="../index.html" class="btn-back"><i class="fas fa-arrow-left"></i> Back to Portfolio</a>
        
        <div class="slide">
            <h1>{title}</h1>
            <h2>{subtitle}</h2>
            <p><strong>Presented for:</strong> {client}</p>
            <p><strong>Presented by:</strong> Senior Director, Cloud Strategy & Architecture, Microsoft</p>
        </div>

        {slides_html}

        <div class="footer">
            <span>Microsoft Confidential | Senior Director, Cloud Strategy & Architecture</span>
            <span>&copy; 2024 Upendra Kumar</span>
        </div>
    </div>
</body>
</html>
"""

presentations = [
    {
        "id": "01-presentation-datacenter-migration",
        "title": "Strategic Data Center Migration & Modernization",
        "subtitle": "Transforming Infrastructure for Agility and Cost Efficiency",
        "client": "Global Tech Firm",
        "slides": [
            {
                "header": "Executive Summary: The Case for Change",
                "content": "<ul><li><strong>30% TCO Reduction:</strong> Projected savings over 3 years by shifting to OpEx.</li><li><strong>Risk Mitigation:</strong> Exit aging data centers; enhance Disaster Recovery.</li><li><strong>Agility:</strong> Enable rapid scaling and modernization post-migration.</li></ul>"
            },
            {
                "header": "Leadership & Strategic Challenges",
                "content": "<ul><li><strong>Stakeholder Alignment:</strong> Negotiated migration windows across 5 business units.</li><li><strong>Cultural Transformation:</strong> Led the shift from 'Server Hugging' to 'Cloud Governance'.</li><li><strong>Risk Mitigation:</strong> Championed a 'Pilot-First' strategy to secure C-level confidence.</li></ul>"
            },
            {
                "header": "Solution Architecture: Secure & Scalable Migration",
                "content": "<ul><li><strong>Azure Migrate:</strong> Centralized discovery, assessment, and migration hub.</li><li><strong>Hybrid Connectivity:</strong> ExpressRoute (Primary) + VPN Gateway (Backup).</li><li><strong>Security:</strong> Identity via Azure AD Hybrid Sync; Encryption at rest.</li></ul>"
            },
            {
                "header": "Visual Journey: The Strategic Path",
                "content": '<img src="../assets/images/projects/01-datacenter-migration-journey.png" alt="Migration Journey">'
            }
        ]
    },
    {
        "id": "02-presentation-landing-zone",
        "title": "Secure Azure Landing Zone Foundation",
        "subtitle": "Accelerating Innovation with Governance and Compliance",
        "client": "FinTech Startup",
        "slides": [
            {
                "header": "Executive Summary: Speed with Control",
                "content": "<ul><li><strong>'Vending Machine' Model:</strong> Reduces provisioning time from weeks to hours.</li><li><strong>Compliance Ready:</strong> Built-in guardrails ensure SOC2/PCI-DSS alignment.</li><li><strong>Scalability:</strong> Hub-and-Spoke topology supports future growth.</li></ul>"
            },
            {
                "header": "Leadership & Strategic Challenges",
                "content": "<ul><li><strong>Governance at Speed:</strong> Implemented 'Policy-as-Code' for automated compliance.</li><li><strong>Organizational Design:</strong> Defined the RACI matrix for the Cloud CCoE.</li><li><strong>Executive Visibility:</strong> Established 'Cloud Governance Scorecards' for the CTO.</li></ul>"
            },
            {
                "header": "Solution Architecture: The 'Vending Machine'",
                "content": "<ul><li><strong>Hub-and-Spoke Network:</strong> Centralized security with Azure Firewall Premium.</li><li><strong>Identity & Access:</strong> Azure AD RBAC with PIM for JIT access.</li><li><strong>Observability:</strong> Azure Sentinel (SIEM) + Log Analytics.</li></ul>"
            },
            {
                "header": "Visual Journey: The Governance Model",
                "content": '<img src="../assets/images/projects/02-landing-zone-governance.png" alt="Governance Model">'
            }
        ]
    },
    {
        "id": "03-presentation-well-architected",
        "title": "Well-Architected Review & Optimization",
        "subtitle": "Maximizing Value and Reliability in Healthcare SaaS",
        "client": "Healthcare SaaS Provider",
        "slides": [
            {
                "header": "Executive Summary: Optimizing for Health",
                "content": "<ul><li><strong>15-20% Cost Savings:</strong> Identified through waste elimination and rightsizing.</li><li><strong>99.99% Reliability:</strong> Elevating architecture to meet critical healthcare SLAs.</li><li><strong>Security:</strong> Enhanced patient data protection via JIT access.</li></ul>"
            },
            {
                "header": "Leadership & Strategic Challenges",
                "content": "<ul><li><strong>Cultural Shift:</strong> Instilled a 'Reliability by Design' culture.</li><li><strong>Financial Accountability:</strong> Partnered with Finance for 'Showback' reporting.</li><li><strong>Crisis Leadership:</strong> Led the 'War Room' response during critical outages.</li></ul>"
            },
            {
                "header": "Solution Architecture: Remediation Plan",
                "content": "<ul><li><strong>Cost Optimization:</strong> Right-size VMs and DBs; implement Azure Advisor.</li><li><strong>Reliability:</strong> Deploy VMSS across Availability Zones; enable GRS.</li><li><strong>Security:</strong> Centralize secrets in Azure Key Vault; enable Defender for Cloud.</li></ul>"
            },
            {
                "header": "Visual Journey: The Optimization Cycle",
                "content": '<img src="../assets/images/projects/03-well-architected-cycle.png" alt="Optimization Cycle">'
            }
        ]
    },
    {
        "id": "04-presentation-app-modernization",
        "title": "Application Modernization Blueprint",
        "subtitle": "Scaling Retail Operations for the Digital Era",
        "client": "Retail Enterprise",
        "slides": [
            {
                "header": "Executive Summary: Ready for Peak Season",
                "content": "<ul><li><strong>Elastic Scalability:</strong> Auto-scale to handle traffic spikes (Black Friday).</li><li><strong>Daily Deployments:</strong> Shift from quarterly to daily releases via CI/CD.</li><li><strong>Performance:</strong> 50% improvement in page load times.</li></ul>"
            },
            {
                "header": "Leadership & Strategic Challenges",
                "content": "<ul><li><strong>DevOps Adoption:</strong> Overcame resistance by demonstrating 90% error reduction.</li><li><strong>Business Continuity:</strong> Orchestrated 'Black Friday' readiness across teams.</li><li><strong>Vendor Management:</strong> Managed 3rd-party integrations for cloud-native compatibility.</li></ul>"
            },
            {
                "header": "Solution Architecture: Cloud-Native PaaS",
                "content": "<ul><li><strong>App Service (PaaS):</strong> Fully managed web hosting with autoscaling.</li><li><strong>Azure SQL Database:</strong> Managed relational DB with high availability.</li><li><strong>Azure Front Door:</strong> Global load balancing and CDN.</li></ul>"
            },
            {
                "header": "Visual Journey: Modernization Pipeline",
                "content": '<img src="../assets/images/projects/04-app-modernization-pipeline.png" alt="Modernization Pipeline">'
            }
        ]
    },
    {
        "id": "05-presentation-ai-analytics",
        "title": "AI-Powered Analytics Platform",
        "subtitle": "Unlocking Business Value with Data & AI",
        "client": "E-Commerce Company",
        "slides": [
            {
                "header": "Executive Summary: From Data to Decisions",
                "content": "<ul><li><strong>Democratized Data:</strong> Unified platform for Engineering, Science, and BI.</li><li><strong>Predictive Power:</strong> AI-driven product recommendations to boost sales.</li><li><strong>Speed:</strong> Reduce insight generation time from days to minutes.</li></ul>"
            },
            {
                "header": "Leadership & Strategic Challenges",
                "content": "<ul><li><strong>Data Governance:</strong> Established Council to resolve ownership disputes.</li><li><strong>Ethical AI:</strong> Authored 'Responsible AI' guidelines for privacy.</li><li><strong>Adoption Drive:</strong> Launched 'Data Academy,' increasing BI adoption by 40%.</li></ul>"
            },
            {
                "header": "Solution Architecture: Modern Data Warehouse",
                "content": "<ul><li><strong>Azure Synapse Analytics:</strong> Unified workspace for Big Data.</li><li><strong>Azure Data Lake Gen2:</strong> Scalable, secure storage.</li><li><strong>Azure Machine Learning:</strong> Build, train, and deploy predictive models.</li></ul>"
            },
            {
                "header": "Visual Journey: Data-to-Value Pipeline",
                "content": '<img src="../assets/images/projects/05-ai-analytics-value-chain.png" alt="Value Chain">'
            }
        ]
    }
]

output_dir = "c:/MyResumePortfolio/presentations"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for p in presentations:
    slides_html = ""
    for slide in p["slides"]:
        slides_html += f"""
        <div class="slide">
            <h3>{slide['header']}</h3>
            <div>{slide['content']}</div>
        </div>
        """
    
    html_content = template.format(
        title=p["title"],
        subtitle=p["subtitle"],
        client=p["client"],
        slides_html=slides_html
    )
    
    file_path = os.path.join(output_dir, f"{p['id']}.html")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Generated {file_path}")
