import os
import re
import datetime
from pathlib import Path
from email.utils import formatdate

# Configuration
BLOG_DIR = r"c:\MyResumePortfolio\blog"
OUTPUT_FILE = r"c:\MyResumePortfolio\feed.xml"
SITE_URL = "https://portfolio.upendrakumar.com"
BLOG_URL_PREFIX = f"{SITE_URL}/blog/"

def parse_html_file(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract Title
    title_match = re.search(r"<title>(.*?)</title>", content, re.IGNORECASE)
    title = title_match.group(1).split("|")[0].strip() if title_match else "No Title"
    
    # Extract Description
    desc_match = re.search(r'<meta\s+name=["\']description["\']\s+content=["\'](.*?)["\']', content, re.IGNORECASE)
    description = desc_match.group(1) if desc_match else "No description available."

    return title, description

def get_date_from_filename(filename):
    # Expecting format: YYYY-MM-DD-title.html
    match = re.match(r"(\d{4}-\d{2}-\d{2})", filename)
    if match:
        return datetime.datetime.strptime(match.group(1), "%Y-%m-%d")
    return datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(BLOG_DIR, filename)))

def generate_rss():
    items = []
    
    # scan files
    files = [f for f in os.listdir(BLOG_DIR) if f.endswith(".html")]
    
    # Sort files by date (newest first) relative to filename
    files.sort(key=lambda x: get_date_from_filename(x), reverse=True)

    for filename in files:
        file_path = os.path.join(BLOG_DIR, filename)
        title, description = parse_html_file(file_path)
        pub_date_dt = get_date_from_filename(filename)
        # Add time to make it valid RFC 822 (e.g. 10:00 AM)
        pub_date_dt = pub_date_dt.replace(hour=10, minute=0)
        pub_date = formatdate(pub_date_dt.timestamp())
        link = f"{BLOG_URL_PREFIX}{filename}"

        item = f"""
        <item>
            <title><![CDATA[{title}]]></title>
            <link>{link}</link>
            <guid>{link}</guid>
            <description><![CDATA[{description}]]></description>
            <pubDate>{pub_date}</pubDate>
        </item>"""
        items.append(item)

    rss_feed = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
    <title>Upendra Kumar | Architecture Insights</title>
    <link>{SITE_URL}</link>
    <description>Expert Azure Architecture, Cloud Strategy, and Technical Leadership insights.</description>
    <language>en-us</language>
    <lastBuildDate>{formatdate(datetime.datetime.now().timestamp())}</lastBuildDate>
    {"".join(items)}
</channel>
</rss>"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(rss_feed)
    
    print(f"Successfully generated {OUTPUT_FILE} with {len(items)} posts.")

if __name__ == "__main__":
    generate_rss()
