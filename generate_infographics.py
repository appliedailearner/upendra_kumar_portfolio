from PIL import Image, ImageDraw, ImageFont
import os

def create_infographic(filename, title, subtitle, points, color_scheme):
    # Image size
    width, height = 1200, 800
    
    # Create image with background color
    img = Image.new('RGB', (width, height), color=color_scheme['bg'])
    draw = ImageDraw.Draw(img)
    
    # Draw a subtle gradient or pattern
    for i in range(height):
        r = int(color_scheme['bg'][0] + (color_scheme['accent'][0] - color_scheme['bg'][0]) * (i / height) * 0.2)
        g = int(color_scheme['bg'][1] + (color_scheme['accent'][1] - color_scheme['bg'][1]) * (i / height) * 0.2)
        b = int(color_scheme['bg'][2] + (color_scheme['accent'][2] - color_scheme['bg'][2]) * (i / height) * 0.2)
        draw.line([(0, i), (width, i)], fill=(r, g, b))

    # Try to load a font, fallback to default
    try:
        title_font = ImageFont.truetype("arial.ttf", 60)
        subtitle_font = ImageFont.truetype("arial.ttf", 35)
        text_font = ImageFont.truetype("arial.ttf", 28)
    except:
        title_font = ImageFont.load_default()
        subtitle_font = ImageFont.load_default()
        text_font = ImageFont.load_default()

    # Draw Title
    draw.text((60, 60), title, font=title_font, fill=color_scheme['text'])
    
    # Draw Subtitle
    draw.text((60, 140), subtitle, font=subtitle_font, fill=color_scheme['accent'])
    
    # Draw a separator line
    draw.line([(60, 200), (width-60, 200)], fill=color_scheme['accent'], width=3)
    
    # Draw Points with icons (circles)
    y_offset = 260
    for point in points:
        # Draw icon circle
        draw.ellipse([(60, y_offset), (90, y_offset+30)], fill=color_scheme['accent'])
        # Draw point text
        draw.text((110, y_offset), point, font=text_font, fill=color_scheme['text'])
        y_offset += 80

    # Draw a "badge" or "result" box at the bottom right
    badge_box = [(width-400, height-150), (width-60, height-60)]
    draw.rectangle(badge_box, fill=color_scheme['accent'], outline=color_scheme['text'], width=2)
    draw.text((width-380, height-120), "STRATEGIC IMPACT", font=text_font, fill=color_scheme['bg'])
    draw.text((width-380, height-90), "Enterprise Ready", font=text_font, fill=color_scheme['bg'])

    # Save the image
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    img.save(filename)
    print(f"Generated {filename}")

# Color Schemes
schemes = {
    'blue': {'bg': (10, 25, 47), 'text': (204, 214, 246), 'accent': (100, 255, 218)},
    'purple': {'bg': (26, 11, 46), 'text': (235, 235, 235), 'accent': (191, 123, 255)},
    'green': {'bg': (11, 31, 17), 'text': (220, 239, 225), 'accent': (82, 255, 140)},
    'orange': {'bg': (31, 18, 11), 'text': (246, 230, 220), 'accent': (255, 160, 100)},
    'teal': {'bg': (11, 31, 31), 'text': (220, 239, 239), 'accent': (100, 255, 255)}
}

projects = [
    {
        'filename': 'assets/images/projects/01-datacenter-migration-journey.png',
        'title': 'Datacenter Migration Journey',
        'subtitle': 'Legacy to Azure Cloud Transformation',
        'points': [
            'Discovery & Assessment of 500+ Virtual Machines',
            'Re-hosting (Lift & Shift) and Re-platforming strategies',
            'Azure Migrate integration for seamless transition',
            '30% TCO Reduction achieved post-migration',
            'Zero downtime migration for critical workloads'
        ],
        'scheme': schemes['blue']
    },
    {
        'filename': 'assets/images/projects/02-landing-zone-governance.png',
        'title': 'Enterprise Azure Landing Zones',
        'subtitle': 'Scalable & Secure Cloud Foundation',
        'points': [
            'Hub-and-Spoke Network Topology implementation',
            'Policy-as-Code for automated compliance',
            'Identity & Access Management (RBAC/PIM)',
            'Centralized Logging and Monitoring (Log Analytics)',
            'Terraform-based Infrastructure Automation'
        ],
        'scheme': schemes['teal']
    },
    {
        'filename': 'assets/images/projects/03-well-architected-cycle.png',
        'title': 'Azure Well-Architected Framework',
        'subtitle': 'Continuous Optimization & Excellence',
        'points': [
            'Cost Optimization: $55K+ annual savings',
            'Operational Excellence: 90% faster deployments',
            'Performance Efficiency: Auto-scaling implementation',
            'Reliability: Multi-region Disaster Recovery',
            'Security: Zero-Trust architecture principles'
        ],
        'scheme': schemes['green']
    },
    {
        'filename': 'assets/images/projects/04-app-modernization-pipeline.png',
        'title': 'App Modernization Pipeline',
        'subtitle': 'Monolith to Microservices Evolution',
        'points': [
            'Containerization using Azure Kubernetes Service (AKS)',
            'CI/CD Pipelines with GitHub Actions',
            'API Management for secure service exposure',
            'Database modernization to Azure SQL/Cosmos DB',
            'Serverless integration with Azure Functions'
        ],
        'scheme': schemes['purple']
    },
    {
        'filename': 'assets/images/projects/05-ai-analytics-value-chain.png',
        'title': 'AI-Powered Analytics',
        'subtitle': 'Data-Driven Decision Intelligence',
        'points': [
            'Azure OpenAI integration for Generative AI',
            'Azure Synapse Analytics for enterprise data warehousing',
            'Real-time streaming with Azure Event Hubs',
            'Power BI dashboards for executive insights',
            'Machine Learning models for predictive maintenance'
        ],
        'scheme': schemes['orange']
    }
]

for project in projects:
    create_infographic(
        project['filename'],
        project['title'],
        project['subtitle'],
        project['points'],
        project['scheme']
    )
