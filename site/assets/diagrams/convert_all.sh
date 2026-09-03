set -euo pipefail
mkdir -p /mnt/data/diagrams/pdf /mnt/data/diagrams/png_hi
for f in /mnt/data/diagrams/vsdx/*.vsdx; do
  base=$(basename "$f" .vsdx)
  echo "[1/2] PDF: $base"
  soffice --headless --convert-to pdf --outdir /mnt/data/diagrams/pdf "$f" >/dev/null 2>&1 || { echo "  soffice failed for $base"; continue; }
  pdf="/mnt/data/diagrams/pdf/${base}.pdf"
  if [ -f "$pdf" ]; then
    echo "[2/2] PNG: $base"
    magick -density 300 "$pdf" -background white -alpha remove -quality 95 "/mnt/data/diagrams/png_hi/${base}.png" >/dev/null 2>&1 || echo "  magick failed for $base"
  else
    echo "  pdf missing for $base"
  fi

done
