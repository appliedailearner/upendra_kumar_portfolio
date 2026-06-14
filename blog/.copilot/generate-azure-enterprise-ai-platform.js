const fs = require('fs');
const path = require('path');

const workspaceRoot = path.resolve(__dirname, '..');
const layoutArg = process.argv[2] || 'azure-enterprise-ai-platform.layout.json';
const outputArg = process.argv[3] || 'azure-enterprise-ai-platform.drawio';
const layoutPath = path.isAbsolute(layoutArg) ? layoutArg : path.join(__dirname, layoutArg);
const outputPath = path.isAbsolute(outputArg) ? outputArg : path.join(__dirname, outputArg);
const localAzureIconRoot = 'C:\\Azure_Public_Service_Icons_V23\\Azure_Public_Service_Icons\\Icons';
const localAzureIconFiles = {
  frontdoor: path.join(localAzureIconRoot, 'networking', '10073-icon-service-Front-Door-and-CDN-Profiles.svg'),
  aisearch: path.join(localAzureIconRoot, 'ai + machine learning', '10044-icon-service-Cognitive-Search.svg')
};

function svgFileToDataUri(filePath) {
  const buffer = fs.readFileSync(filePath);
  return `data:image/svg+xml;base64,${buffer.toString('base64')}`;
}

const iconMap = {
  ...JSON.parse(fs.readFileSync(path.join(workspaceRoot, '.icon-data.json'), 'utf8')),
  ...Object.fromEntries(
    Object.entries(localAzureIconFiles)
      .filter(([, filePath]) => fs.existsSync(filePath))
      .map(([key, filePath]) => [key, svgFileToDataUri(filePath)])
  )
};
const layout = JSON.parse(fs.readFileSync(layoutPath, 'utf8'));

function esc(value = '') {
  return String(value)
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;')
    .replace(/\n/g, '&#xa;');
}

function attrs(obj) {
  return Object.entries(obj)
    .filter(([, value]) => value !== undefined && value !== null && value !== '')
    .map(([key, value]) => ` ${key}="${esc(value)}"`)
    .join('');
}

function geometry(x, y, width, height, points) {
  if (points && points.length) {
    const pointXml = points.map((point) => `<mxPoint x="${point.x}" y="${point.y}"/>`).join('');
    return `<mxGeometry x="${x}" y="${y}" width="${width}" height="${height}" relative="1" as="geometry"><Array as="points">${pointXml}</Array></mxGeometry>`;
  }

  return `<mxGeometry x="${x}" y="${y}" width="${width}" height="${height}" as="geometry"/>`;
}

function edgeGeometry(points) {
  if (points && points.length) {
    const pointXml = points.map((point) => `<mxPoint x="${point.x}" y="${point.y}"/>`).join('');
    return `<mxGeometry relative="1" as="geometry"><Array as="points">${pointXml}</Array></mxGeometry>`;
  }

  return '<mxGeometry relative="1" as="geometry"/>';
}

function sectionStyle(fillColor, strokeColor) {
  return [
    'swimlane',
    'html=1',
    'rounded=1',
    'startSize=36',
    'fillColor=' + fillColor,
    'strokeColor=' + strokeColor,
    'fontStyle=1',
    'fontSize=16',
    'container=1',
    'horizontal=0',
    'whiteSpace=wrap'
  ].join(';');
}

function laneStyle() {
  return [
    'swimlane',
    'html=1',
    'rounded=1',
    'startSize=30',
    'fillColor=#ffffff',
    'strokeColor=#cbd5e1',
    'fontStyle=1',
    'fontSize=14',
    'container=1',
    'horizontal=0',
    'whiteSpace=wrap'
  ].join(';');
}

function noteStyle(fillColor, strokeColor, fontColor) {
  return [
    'rounded=1',
    'whiteSpace=wrap',
    'html=1',
    'spacing=10',
    'align=left',
    'verticalAlign=top',
    'fontSize=12',
    'fillColor=' + fillColor,
    'strokeColor=' + strokeColor,
    'fontColor=' + fontColor
  ].join(';');
}

function serviceStyle(fillColor = '#eff6ff', strokeColor = '#93c5fd', fontColor = '#1e3a8a') {
  return [
    'rounded=1',
    'whiteSpace=wrap',
    'html=1',
    'spacing=8',
    'align=center',
    'verticalAlign=middle',
    'fontSize=12',
    'fillColor=' + fillColor,
    'strokeColor=' + strokeColor,
    'fontColor=' + fontColor
  ].join(';');
}

function azureServiceCardStyle() {
  return serviceStyle('#eff6ff', '#2563eb', '#1d4ed8');
}

function imageStyle(iconKey) {
  const image = iconMap[iconKey];
  if (!image) {
    throw new Error(`Missing icon key: ${iconKey}`);
  }

  if (!image.startsWith('data:image/')) {
    throw new Error(`Icon key ${iconKey} is not a local embedded image`);
  }

  return [
    'shape=image',
    'html=1',
    'verticalLabelPosition=bottom',
    'verticalAlign=top',
    'imageAspect=0',
    'aspect=fixed',
    'fontSize=11',
    'spacingTop=6',
    'image=' + image
  ].join(';');
}

function edgeStyle(kind) {
  const styles = {
    active: 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#2563eb;strokeWidth=2;endArrow=block;endFill=1;',
    private: 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#0f766e;strokeWidth=2;endArrow=block;endFill=1;',
    sync: 'edgeStyle=orthogonalEdgeStyle;rounded=0;orthogonalLoop=1;jettySize=auto;html=1;strokeColor=#7c3aed;strokeWidth=2;dashed=1;endArrow=block;endFill=1;'
  };

  return styles[kind] || styles.active;
}

const cells = ['<mxCell id="0"/>', '<mxCell id="1" parent="0"/>'];

function validateNodePolicy(node) {
  const isAzureService = Boolean(node.isAzureService);
  const iconRequired = Boolean(node.iconRequired);
  const fallbackAllowed = Boolean(node.fallbackAllowed);
  const hasIconKey = Boolean(node.iconKey);
  const hasLocalIcon = hasIconKey && Boolean(iconMap[node.iconKey]);
  const usesImage = node.kind === 'image';

  const result = {
    id: node.id,
    label: node.label,
    serviceType: node.serviceType || null,
    isAzureService,
    iconRequired,
    fallbackAllowed,
    kind: node.kind,
    iconKey: node.iconKey || null,
    hasLocalIcon,
    compliant: true,
    message: 'ok'
  };

  if (!node.serviceType) {
    throw new Error(`Node ${node.id} is missing required serviceType metadata`);
  }

  if (!isAzureService && iconRequired) {
    throw new Error(`Node ${node.id} cannot require an icon when isAzureService=false`);
  }

  if (!isAzureService && !fallbackAllowed && !usesImage) {
    throw new Error(`Abstract node ${node.id} must explicitly allow fallback when it is not rendered as an image`);
  }

  if (usesImage && !hasIconKey) {
    throw new Error(`Image node ${node.id} is missing iconKey`);
  }

  if (usesImage && !hasLocalIcon) {
    throw new Error(`Image node ${node.id} references missing local icon key ${node.iconKey}`);
  }

  if (iconRequired && !usesImage) {
    result.compliant = false;
    result.message = 'icon required but node is not rendered as an image';
    throw new Error(`Azure service ${node.id} must use a local standard Azure icon`);
  }

  if (iconRequired && !hasLocalIcon) {
    result.compliant = false;
    result.message = 'icon required but local icon is missing';
    throw new Error(`Azure service ${node.id} requires a local icon but iconKey ${node.iconKey} is unavailable`);
  }

  if (isAzureService && usesImage && !iconRequired) {
    result.message = 'azure service uses local icon as optional enhancement';
  }

  if (isAzureService && !usesImage) {
    if (!fallbackAllowed) {
      result.compliant = false;
      result.message = 'fallback card is not allowed for this Azure service';
      throw new Error(`Azure service ${node.id} cannot use a fallback card`);
    }

    result.message = hasLocalIcon
      ? 'non-compliant fallback: local icon exists and should be used'
      : 'approved fallback: no local icon exists in .icon-data.json';

    if (hasLocalIcon) {
      result.compliant = false;
      throw new Error(`Azure service ${node.id} has local icon ${node.iconKey} and must not use a fallback card`);
    }
  }

  return result;
}

const iconAudit = layout.nodes.map(validateNodePolicy);

function addVertex({ id, parent = '1', value = '', style, x, y, w, h }) {
  cells.push(`<mxCell${attrs({ id, value, style, vertex: '1', parent })}>${geometry(x, y, w, h)}</mxCell>`);
}

function addEdge({ id, source, target, kind, points }) {
  cells.push(`<mxCell${attrs({ id, style: edgeStyle(kind), edge: '1', parent: '1', source, target })}>${edgeGeometry(points)}</mxCell>`);
}

addVertex({
  id: 'title',
  value: `${layout.title}\n<font style="font-size:14px;color:#475569;">${layout.subtitle}</font>`,
  style: 'text;html=1;strokeColor=none;fillColor=none;align=left;verticalAlign=middle;whiteSpace=wrap;fontSize=24;fontStyle=1;fontColor=#0f172a;',
  x: 20,
  y: 20,
  w: 1000,
  h: 60
});

layout.containers.forEach((container) => {
  const style = container.kind === 'lane'
    ? laneStyle()
    : sectionStyle(container.fillColor, container.strokeColor);

  addVertex({
    id: container.id,
    parent: container.parent || '1',
    value: container.label,
    style,
    x: container.x,
    y: container.y,
    w: container.w,
    h: container.h
  });
});

layout.nodes.forEach((node) => {
  let style;
  if (node.kind === 'image') {
    style = imageStyle(node.iconKey);
  } else if (node.kind === 'service-azure') {
    style = azureServiceCardStyle();
  } else if (node.kind === 'service-gold') {
    style = serviceStyle('#fefce8', '#f59e0b', '#92400e');
  } else if (node.kind === 'service-purple') {
    style = serviceStyle('#f5f3ff', '#a78bfa', '#5b21b6');
  } else if (node.kind === 'service-green') {
    style = serviceStyle('#ecfdf5', '#34d399', '#166534');
  } else if (node.kind === 'anchor') {
    style = serviceStyle('#ffffff', '#cbd5e1', '#0f172a');
  } else {
    style = serviceStyle();
  }

  addVertex({
    id: node.id,
    parent: node.parent,
    value: node.label,
    style,
    x: node.x,
    y: node.y,
    w: node.w,
    h: node.h
  });
});

layout.notes.forEach((note) => {
  addVertex({
    id: note.id,
    parent: note.parent,
    value: note.label,
    style: noteStyle(note.fillColor, note.strokeColor, note.fontColor),
    x: note.x,
    y: note.y,
    w: note.w,
    h: note.h
  });
});

layout.edges.forEach(addEdge);

const xml = `<mxGraphModel dx="1540" dy="900" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" pageWidth="2200" pageHeight="1400" math="0" shadow="0"><root>${cells.join('')}</root></mxGraphModel>`;

const outPath = outputPath;
const auditPath = path.join(path.dirname(outPath), `${path.basename(outPath, path.extname(outPath))}.icon-audit.json`);
fs.writeFileSync(outPath, xml, 'utf8');
fs.writeFileSync(auditPath, JSON.stringify({
  generatedAt: new Date().toISOString(),
  layoutFile: path.basename(layoutPath),
  outputFile: path.basename(outPath),
  summary: {
    totalNodes: iconAudit.length,
    azureServiceNodes: iconAudit.filter((entry) => entry.isAzureService).length,
    iconRequiredNodes: iconAudit.filter((entry) => entry.iconRequired).length,
    approvedFallbackNodes: iconAudit.filter((entry) => entry.message === 'approved fallback: no local icon exists in .icon-data.json').length
  },
  nodes: iconAudit
}, null, 2), 'utf8');
console.log(`Generated ${outPath}`);
console.log(`Generated ${auditPath}`);
