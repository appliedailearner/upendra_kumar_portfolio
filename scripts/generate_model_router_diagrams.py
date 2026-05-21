import base64
import os
from pathlib import Path


ROOT = Path(r"C:\MyResumePortfolio")
ICON_ROOT = ROOT / "blog" / "assets" / "Azure_Public_Service_Icons" / "Icons"
OUT_DIR = ROOT / "images" / "blog"


ICON_FILES = {
    "apim": "10042-icon-service-API-Management-Services.svg",
    "openai": "03438-icon-service-Azure-OpenAI.svg",
    "search": "10044-icon-service-Cognitive-Search.svg",
    "private_endpoint": "02579-icon-service-Private-Endpoints.svg",
    "managed_identity": "10227-icon-service-Managed-Identities.svg",
    "key_vault": "10245-icon-service-Key-Vaults.svg",
    "vnet": "10061-icon-service-Virtual-Networks.svg",
    "front_door": "10073-icon-service-Front-Door-and-CDN-Profiles.svg",
    "app_gateway": "10076-icon-service-Application-Gateways.svg",
    "ai_studio": "03513-icon-service-AI-Studio.svg",
}


def find_icon(filename: str) -> Path:
    for path in ICON_ROOT.rglob(filename):
        return path
    raise FileNotFoundError(filename)


def data_uri(filename: str) -> str:
    path = find_icon(filename)
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


ICONS = {key: data_uri(name) for key, name in ICON_FILES.items()}


def icon_with_label(
    href: str,
    x: int,
    y: int,
    label: str,
    sublabel: str = "",
    size: int = 56,
    label_width: int = 180,
) -> str:
    label_lines = label.split("\n")
    text_y = y + size + 26
    parts = [
        f'<image href="{href}" x="{x}" y="{y}" width="{size}" height="{size}"/>'
    ]
    for idx, line in enumerate(label_lines):
        parts.append(
            f'<text class="node-label" x="{x + (label_width / 2)}" y="{text_y + idx * 18}" '
            f'text-anchor="middle">{line}</text>'
        )
    if sublabel:
        parts.append(
            f'<text class="node-sub" x="{x + (label_width / 2)}" y="{text_y + len(label_lines) * 18 + 18}" '
            f'text-anchor="middle">{sublabel}</text>'
        )
    return "\n".join(parts)


def card(x: int, y: int, w: int, h: int, title: str, subtitle: str = "", kind: str = "card") -> str:
    title_y = y + 28
    subtitle_svg = (
        f'<text class="card-sub" x="{x + 18}" y="{title_y + 20}">{subtitle}</text>' if subtitle else ""
    )
    return f"""
    <rect class="{kind}" x="{x}" y="{y}" width="{w}" height="{h}" rx="18"/>
    <text class="card-title" x="{x + 18}" y="{title_y}">{title}</text>
    {subtitle_svg}
    """


def write_svg(name: str, body: str, width: int, height: int, title: str, desc: str) -> None:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <defs>
    <style>
      text {{ font-family: "Segoe UI", Arial, sans-serif; fill: #1b1b1b; }}
      .bg {{ fill: #f8fbff; }}
      .frame {{ fill: #ffffff; stroke: #d5e3f0; stroke-width: 1.5; }}
      .section {{ fill: #ffffff; stroke: #b7d3ea; stroke-width: 1.5; }}
      .group {{ fill: #f7fbff; stroke: #8fbbe0; stroke-width: 1.6; stroke-dasharray: 8 6; }}
      .group-soft {{ fill: #fbfdff; stroke: #c8d7e6; stroke-width: 1.4; }}
      .card {{ fill: #ffffff; stroke: #93b4d1; stroke-width: 1.5; }}
      .accent-card {{ fill: #f3f9ff; stroke: #6ea8d8; stroke-width: 1.6; }}
      .secure-card {{ fill: #f5fbf8; stroke: #7cbc9d; stroke-width: 1.6; }}
      .public-card {{ fill: #fff8f2; stroke: #dfb687; stroke-width: 1.4; }}
      .card-title {{ font-size: 24px; font-weight: 700; fill: #0f3b68; }}
      .card-sub {{ font-size: 14px; fill: #486581; }}
      .hero-title {{ font-size: 34px; font-weight: 700; fill: #0f3b68; }}
      .hero-sub {{ font-size: 16px; fill: #486581; }}
      .node-label {{ font-size: 15px; font-weight: 700; fill: #0f3b68; }}
      .node-sub {{ font-size: 12px; fill: #5d7288; }}
      .mini {{ font-size: 13px; fill: #4f6376; }}
      .smallcaps {{ font-size: 12px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; fill: #0f6cbd; }}
      .badge {{ fill: #e8f3ff; stroke: #9fc5ea; stroke-width: 1; }}
      .badge-text {{ font-size: 12px; font-weight: 700; fill: #0f6cbd; }}
      .arrow {{ stroke: #2573b8; stroke-width: 3.5; fill: none; marker-end: url(#arrowBlue); }}
      .arrow-soft {{ stroke: #2573b8; stroke-width: 2.6; fill: none; marker-end: url(#arrowBlue); stroke-dasharray: 8 6; }}
      .arrow-secure {{ stroke: #2e8b57; stroke-width: 3; fill: none; marker-end: url(#arrowGreen); }}
      .line {{ stroke: #7a94ad; stroke-width: 2; fill: none; }}
    </style>
    <marker id="arrowBlue" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#2573b8"/>
    </marker>
    <marker id="arrowGreen" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto">
      <path d="M0,0 L10,5 L0,10 z" fill="#2e8b57"/>
    </marker>
  </defs>
  <rect class="bg" x="0" y="0" width="{width}" height="{height}" rx="28"/>
  {body}
</svg>
"""
    (OUT_DIR / name).write_text(svg, encoding="utf-8")


enterprise_body = f"""
  <rect class="frame" x="24" y="24" width="1552" height="852" rx="26"/>
  <rect class="section" x="54" y="92" width="320" height="712" rx="20"/>
  <text class="smallcaps" x="76" y="124">Consumer layer</text>
  {icon_with_label(ICONS["front_door"], 104, 196, "Client or app", "Interactive request origin", 62, 170)}
  <path class="arrow" d="M196 306 H 270"/>
  <rect class="accent-card" x="258" y="224" width="88" height="164" rx="18"/>
  <text class="node-label" x="302" y="266" text-anchor="middle">HTTPS</text>
  <text class="mini" x="302" y="292" text-anchor="middle">JWT bearer token</text>
  <text class="mini" x="302" y="316" text-anchor="middle">client metadata</text>
  <text class="mini" x="302" y="340" text-anchor="middle">conversation context</text>

  <rect class="section" x="404" y="92" width="398" height="712" rx="20"/>
  <text class="smallcaps" x="426" y="124">Gateway layer</text>
  <rect class="accent-card" x="450" y="176" width="306" height="248" rx="22"/>
  {icon_with_label(ICONS["apim"], 572, 268, "Azure API Management", "Policy and trust boundary", 68, 120)}
  <rect class="group-soft" x="478" y="304" width="250" height="94" rx="16"/>
  <text class="node-label" x="603" y="334" text-anchor="middle">Core controls</text>
  <text class="mini" x="603" y="356" text-anchor="middle">JWT validation, rate limits, retries</text>
  <text class="mini" x="603" y="376" text-anchor="middle">routing headers, observability, DR policy</text>
  <path class="arrow" d="M756 300 H 826"/>
  <rect class="badge" x="460" y="454" width="286" height="34" rx="17"/>
  <text class="badge-text" x="603" y="476" text-anchor="middle">APIM backend pools map to router deployments</text>

  <rect class="section" x="832" y="92" width="690" height="712" rx="20"/>
  <text class="smallcaps" x="854" y="124">AI services VNet</text>
  <rect class="group" x="864" y="152" width="624" height="604" rx="22"/>
  <text class="card-title" x="886" y="188">Routing and model layer</text>
  <text class="card-sub" x="886" y="212">Model Router remains private and receives traffic only from the approved gateway path</text>

  <rect class="accent-card" x="918" y="286" width="220" height="164" rx="22"/>
  {icon_with_label(ICONS["ai_studio"], 1000, 308, "Azure AI Foundry", "Model Router deployment", 70, 150)}

  <rect class="group-soft" x="1190" y="248" width="248" height="396" rx="18"/>
  <text class="card-title" x="1214" y="282">Approved model pool</text>
  {icon_with_label(ICONS["openai"], 1232, 318, "GPT-4o", "Primary high-capability path", 56, 120)}
  {icon_with_label(ICONS["openai"], 1338, 318, "GPT-4.1 mini", "Low-cost request class", 56, 120)}
  {icon_with_label(ICONS["openai"], 1232, 456, "Reasoning model", "Complex planning class", 56, 120)}
  {icon_with_label(ICONS["search"], 1338, 456, "Search or tool layer", "Grounded retrieval path", 56, 120)}

  <path class="arrow" d="M1138 338 H 1190"/>
  <path class="arrow-soft" d="M1138 372 H 1190"/>
  <path class="arrow-soft" d="M1138 406 H 1190"/>
  <path class="arrow-soft" d="M1138 440 H 1190"/>

  <rect class="badge" x="936" y="610" width="470" height="34" rx="17"/>
  <text class="badge-text" x="1171" y="632" text-anchor="middle">Routing decision uses policy metadata, request class, and approved deployment rules</text>

  <path class="arrow" d="M346 306 H 450"/>
  <text class="mini" x="390" y="290" text-anchor="middle">Validated request</text>
  <text class="mini" x="790" y="290" text-anchor="middle">Backend call</text>
"""


network_body = f"""
  <rect class="frame" x="24" y="24" width="1552" height="1052" rx="26"/>
  <rect class="public-card" x="64" y="92" width="260" height="930" rx="20"/>
  <text class="smallcaps" x="86" y="124">Public and edge zone</text>
  {icon_with_label(ICONS["front_door"], 128, 190, "Azure Front Door", "Optional global edge", 66, 130)}
  <path class="arrow" d="M160 320 V 374"/>
  {icon_with_label(ICONS["app_gateway"], 128, 394, "Application Gateway", "WAF enforced ingress", 66, 130)}
  <rect class="badge" x="94" y="590" width="200" height="36" rx="18"/>
  <text class="badge-text" x="194" y="613" text-anchor="middle">No direct public access to Model Router</text>

  <rect class="section" x="356" y="92" width="1180" height="930" rx="20"/>
  <text class="smallcaps" x="378" y="124">Private Azure boundary</text>
  <rect class="group" x="392" y="152" width="1108" height="834" rx="24"/>
  {icon_with_label(ICONS["vnet"], 432, 236, "Virtual network", "Segregated AI services VNet", 58, 120)}

  <rect class="group-soft" x="432" y="346" width="300" height="250" rx="18"/>
  <text class="card-title" x="454" y="378">Ingress subnet</text>
  {icon_with_label(ICONS["apim"], 488, 406, "Azure API Management", "Internal gateway mode", 68, 180)}

  <rect class="group-soft" x="432" y="632" width="300" height="258" rx="18"/>
  <text class="card-title" x="454" y="664">Identity and secrets</text>
  {icon_with_label(ICONS["managed_identity"], 468, 712, "Managed identity", "APIM to router authorization", 58, 150)}
  {icon_with_label(ICONS["key_vault"], 592, 712, "Key Vault", "Certificates and secret material", 58, 120)}
  <path class="arrow-secure" d="M556 792 H 620"/>

  <rect class="group-soft" x="794" y="346" width="300" height="250" rx="18"/>
  <text class="card-title" x="816" y="378">Private routing subnet</text>
  {icon_with_label(ICONS["private_endpoint"], 846, 408, "Private endpoint", "Inbound access to router", 64, 160)}
  {icon_with_label(ICONS["ai_studio"], 958, 408, "Azure AI Foundry", "Model Router deployment", 64, 160)}
  <path class="arrow" d="M910 440 H 956"/>

  <rect class="group-soft" x="1154" y="346" width="296" height="544" rx="18"/>
  <text class="card-title" x="1176" y="378">Private AI dependencies</text>
  {icon_with_label(ICONS["openai"], 1188, 432, "Azure OpenAI", "Approved model deployments", 62, 150)}
  {icon_with_label(ICONS["search"], 1304, 432, "Azure AI Search", "Retrieval and grounding", 62, 140)}
  {icon_with_label(ICONS["private_endpoint"], 1188, 610, "Private endpoint", "OpenAI private link", 58, 150)}
  {icon_with_label(ICONS["private_endpoint"], 1304, 610, "Private endpoint", "Search private link", 58, 140)}

  <path class="arrow" d="M119 320 H 194"/>
  <path class="arrow" d="M194 462 H 432"/>
  <path class="arrow" d="M732 470 H 794"/>
  <path class="arrow" d="M1094 470 H 1154"/>
  <path class="arrow-secure" d="M582 742 V 540 H 488"/>
  <path class="arrow-secure" d="M1040 508 V 620 H 1188"/>
  <path class="arrow-secure" d="M1040 508 V 620 H 1304"/>

  <rect class="secure-card" x="794" y="632" width="656" height="170" rx="18"/>
  <text class="card-title" x="818" y="666">Security controls that matter</text>
  <text class="mini" x="818" y="696">1. APIM authenticates callers before traffic reaches the router layer.</text>
  <text class="mini" x="818" y="722">2. Managed identity replaces shared secrets for service-to-service authorization.</text>
  <text class="mini" x="818" y="748">3. Private endpoints constrain traffic to the VNet and eliminate public exposure of backend AI services.</text>
  <text class="mini" x="818" y="774">4. Key Vault centralizes certificate and secret management for gateway dependencies.</text>
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_svg(
        "azure_enterprise_ai_architecture_v2.svg",
        enterprise_body,
        1600,
        900,
        "Enterprise AI Routing Pattern",
        "Azure reference architecture style diagram showing APIM in front of Azure AI Foundry Model Router and a governed model pool.",
    )
    write_svg(
        "azure_secure_network_topology_v2.svg",
        network_body,
        1600,
        1100,
        "Secure Network Topology for Azure Model Router",
        "Azure reference architecture style diagram showing Front Door, Application Gateway, internal APIM, managed identity, private endpoint, Model Router, Azure OpenAI, Azure AI Search, and Key Vault.",
    )
    print("Generated model router SVG diagrams.")


if __name__ == "__main__":
    main()
