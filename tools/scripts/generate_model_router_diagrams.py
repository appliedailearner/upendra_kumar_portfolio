import base64
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
    encoded = base64.b64encode(find_icon(filename).read_bytes()).decode("ascii")
    return f"data:image/svg+xml;base64,{encoded}"


ICONS = {key: data_uri(name) for key, name in ICON_FILES.items()}


def icon_with_label(
    href: str,
    x: int,
    y: int,
    label: str,
    sublabel: str = "",
    size: int = 60,
    label_width: int = 160,
) -> str:
    text_y = y + size + 24
    parts = [f'<image href="{href}" x="{x}" y="{y}" width="{size}" height="{size}"/>']
    parts.append(
        f'<text class="node-label" x="{x + (label_width / 2)}" y="{text_y}" text-anchor="middle">{label}</text>'
    )
    if sublabel:
        parts.append(
            f'<text class="node-sub" x="{x + (label_width / 2)}" y="{text_y + 24}" text-anchor="middle">{sublabel}</text>'
        )
    return "\n".join(parts)


def write_svg(name: str, body: str, width: int, height: int, title: str, desc: str) -> None:
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">
  <title id="title">{title}</title>
  <desc id="desc">{desc}</desc>
  <defs>
    <style>
      text {{ font-family: "Segoe UI", Arial, sans-serif; fill: #1b1b1b; }}
      .bg {{ fill: #f8fbff; }}
      .frame {{ fill: #ffffff; stroke: #d5e3f0; stroke-width: 1.5; }}
      .section {{ fill: #ffffff; stroke: #bfd8ec; stroke-width: 1.4; }}
      .group {{ fill: #f7fbff; stroke: #9ec4e3; stroke-width: 1.4; stroke-dasharray: 7 5; }}
      .group-soft {{ fill: #fbfdff; stroke: #d7e3ef; stroke-width: 1.2; }}
      .accent-card {{ fill: #f3f9ff; stroke: #6ea8d8; stroke-width: 1.5; }}
      .secure-card {{ fill: #f5fbf8; stroke: #7cbc9d; stroke-width: 1.5; }}
      .public-card {{ fill: #fff8f2; stroke: #dfb687; stroke-width: 1.3; }}
      .card-title {{ font-size: 22px; font-weight: 700; fill: #0f3b68; }}
      .card-sub {{ font-size: 13px; fill: #4d657d; }}
      .node-label {{ font-size: 16px; font-weight: 700; fill: #0f3b68; }}
      .node-sub {{ font-size: 12px; fill: #61788f; }}
      .mini {{ font-size: 12px; fill: #51677d; }}
      .smallcaps {{ font-size: 12px; font-weight: 700; letter-spacing: 1.2px; text-transform: uppercase; fill: #0f6cbd; }}
      .badge {{ fill: #e8f3ff; stroke: #9fc5ea; stroke-width: 1; }}
      .badge-text {{ font-size: 12px; font-weight: 700; fill: #0f6cbd; }}
      .arrow {{ stroke: #2573b8; stroke-width: 3.3; fill: none; marker-end: url(#arrowBlue); }}
      .arrow-soft {{ stroke: #2573b8; stroke-width: 2.4; fill: none; marker-end: url(#arrowBlue); stroke-dasharray: 8 6; }}
      .arrow-secure {{ stroke: #2e8b57; stroke-width: 2.8; fill: none; marker-end: url(#arrowGreen); }}
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
  <rect class="frame" x="24" y="24" width="1552" height="772" rx="26"/>

  <rect class="section" x="54" y="104" width="264" height="600" rx="20"/>
  <text class="smallcaps" x="76" y="138">1. Consumer</text>
  {icon_with_label(ICONS["front_door"], 116, 250, "Client applications", "Interactive and API workloads", 72, 140)}

  <rect class="section" x="364" y="104" width="396" height="600" rx="20"/>
  <text class="smallcaps" x="386" y="138">2. Governance gateway</text>
  <rect class="accent-card" x="438" y="224" width="248" height="214" rx="22"/>
  {icon_with_label(ICONS["apim"], 528, 248, "Azure API Management", "Auth, policy, quota, observability", 72, 160)}
  <rect class="badge" x="458" y="498" width="208" height="32" rx="16"/>
  <text class="badge-text" x="562" y="519" text-anchor="middle">Single enterprise control point</text>

  <rect class="section" x="806" y="104" width="718" height="600" rx="20"/>
  <text class="smallcaps" x="828" y="138">3. Private AI services VNet</text>
  <rect class="accent-card" x="878" y="236" width="240" height="204" rx="22"/>
  {icon_with_label(ICONS["ai_studio"], 966, 260, "Azure AI Foundry", "Model Router endpoint", 74, 150)}

  <rect class="group-soft" x="1188" y="206" width="270" height="292" rx="20"/>
  <text class="card-title" x="1210" y="242">Approved model pool</text>
  {icon_with_label(ICONS["openai"], 1216, 292, "GPT-4o", "Premium path", 60, 120)}
  {icon_with_label(ICONS["openai"], 1324, 292, "GPT-4.1 mini", "Lower-cost path", 60, 120)}
  {icon_with_label(ICONS["search"], 1270, 404, "Grounded search/tool path", "Retrieval-backed requests", 60, 160)}

  <path class="arrow" d="M210 354 H 364"/>
  <path class="arrow" d="M760 354 H 878"/>
  <path class="arrow" d="M1118 326 H 1188"/>
  <path class="arrow-soft" d="M1118 362 H 1188"/>
  <path class="arrow-soft" d="M1118 398 H 1248"/>

  <rect class="secure-card" x="878" y="556" width="580" height="104" rx="18"/>
  <text class="card-title" x="902" y="592">Design intent</text>
  <text class="mini" x="902" y="618">APIM stays in front of the router, and the router selects only from an approved backend pool.</text>
  <text class="mini" x="902" y="640">Retry, failover, and audit controls stay in the gateway and orchestration layers.</text>
"""


network_body = f"""
  <rect class="frame" x="24" y="24" width="1552" height="972" rx="26"/>

  <rect class="public-card" x="64" y="118" width="242" height="696" rx="20"/>
  <text class="smallcaps" x="86" y="152">Public edge</text>
  {icon_with_label(ICONS["front_door"], 116, 232, "Azure Front Door", "Optional", 66, 130)}
  {icon_with_label(ICONS["app_gateway"], 116, 432, "Application Gateway", "WAF ingress", 66, 130)}
  <path class="arrow" d="M149 358 V 414"/>
  <rect class="badge" x="90" y="660" width="188" height="32" rx="16"/>
  <text class="badge-text" x="184" y="681" text-anchor="middle">Public traffic ends here</text>

  <rect class="section" x="352" y="118" width="1184" height="696" rx="20"/>
  <text class="smallcaps" x="374" y="152">Private Azure boundary</text>
  <rect class="group" x="390" y="188" width="1110" height="588" rx="22"/>
  {icon_with_label(ICONS["vnet"], 432, 214, "AI services VNet", "Private-only service path", 58, 120)}

  <rect class="accent-card" x="452" y="316" width="230" height="188" rx="22"/>
  {icon_with_label(ICONS["apim"], 532, 340, "Internal APIM", "Authenticated gateway", 70, 150)}

  <rect class="accent-card" x="816" y="316" width="248" height="188" rx="22"/>
  {icon_with_label(ICONS["private_endpoint"], 856, 340, "Private endpoint", "Router ingress", 64, 150)}
  {icon_with_label(ICONS["ai_studio"], 960, 340, "Model Router", "Azure AI Foundry", 64, 130)}

  <rect class="group-soft" x="1140" y="282" width="298" height="254" rx="20"/>
  <text class="card-title" x="1164" y="316">Private AI dependencies</text>
  {icon_with_label(ICONS["openai"], 1178, 366, "Azure OpenAI", "Private access", 60, 140)}
  {icon_with_label(ICONS["search"], 1290, 366, "Azure AI Search", "Private access", 60, 140)}

  <rect class="group-soft" x="452" y="570" width="286" height="150" rx="20"/>
  <text class="card-title" x="476" y="604">Identity and secrets</text>
  {icon_with_label(ICONS["managed_identity"], 492, 632, "Managed identity", "", 56, 120)}
  {icon_with_label(ICONS["key_vault"], 608, 632, "Key Vault", "", 56, 120)}

  <path class="arrow" d="M182 446 H 452"/>
  <path class="arrow" d="M682 410 H 816"/>
  <path class="arrow" d="M1064 410 H 1140"/>
  <path class="arrow-secure" d="M552 660 V 518 H 532"/>

  <rect class="secure-card" x="816" y="580" width="622" height="128" rx="18"/>
  <text class="card-title" x="842" y="616">Security outcome</text>
  <text class="mini" x="842" y="642">The router is never internet-facing. APIM handles policy, managed identity handles trust, and private endpoints keep traffic inside the VNet.</text>
  <text class="mini" x="842" y="666">This is the minimum enterprise pattern for explaining private AI access without overwhelming the reader.</text>
"""


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    write_svg(
        "azure_enterprise_ai_architecture_v2.svg",
        enterprise_body,
        1600,
        820,
        "Enterprise AI Routing Pattern",
        "Azure reference architecture style diagram showing APIM in front of Azure AI Foundry Model Router and a governed model pool.",
    )
    write_svg(
        "azure_secure_network_topology_v2.svg",
        network_body,
        1600,
        1020,
        "Secure Network Topology for Azure Model Router",
        "Azure reference architecture style diagram showing Front Door, Application Gateway, internal APIM, managed identity, private endpoint, Model Router, Azure OpenAI, and Azure AI Search.",
    )
    print("Generated model router SVG diagrams.")


if __name__ == "__main__":
    main()
