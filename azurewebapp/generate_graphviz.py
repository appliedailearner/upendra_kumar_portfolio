from graphviz import Digraph

dot = Digraph(comment='App Service Private-Only Architecture')

dot.attr('graph', rankdir='LR', splines='ortho', nodesep='0.8', ranksep='1.2', fontname='Segoe UI')
dot.attr('node', shape='box', style='rounded,filled', fontname='Segoe UI', fontsize='10', color='#0078D4', fillcolor='#EBF3FC')
dot.attr('edge', fontname='Segoe UI', fontsize='9', color='#605E5C')

dot.node('Client', 'Users / Internet Clients', shape='ellipse', fillcolor='#F3F2F1', color='#8A8886')

with dot.subgraph(name='cluster_vnet') as vnet:
    vnet.attr(label='Virtual Network: vnet-ictsi-sea-01', style='dashed', color='#0078D4', bgcolor='#F8F8F8', fontcolor='#0078D4')
    vnet.node('APIM', 'Azure API Management\n(External/Internal VNet Mode)')
    vnet.node('PE', 'Azure Private Endpoint\nIP: 10.50.10.x')

with dot.subgraph(name='cluster_paas') as paas:
    paas.attr(label='Azure PaaS Services', style='dashed', color='#107C10', bgcolor='#F3F9F1', fontcolor='#107C10')
    paas.node('AppServer', 'Azure App Service Web App\nPublic Access: Disabled!', color='#D13438', fillcolor='#FDE7E9', fontcolor='#A4262C')

dot.node('DNS', 'Private DNS Zone\nprivatelink.azurewebsites.net', color='#8764B8', fillcolor='#F3F0F9')

dot.edge('Client', 'APIM', label=' HTTPS Request')
dot.edge('APIM', 'PE', label=' Routes to Private IP')
dot.edge('PE', 'AppServer', label=' Private Link')
dot.edge('APIM', 'DNS', label=' Resolves Backend Name', style='dashed')

dot.render('architecture_diagram', format='png', cleanup=True)
print("Graphviz PNG generated at architecture_diagram.png")
