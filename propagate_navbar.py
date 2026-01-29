import os
import re

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Skip if already processed or if it's not a proper HTML file
    if 'id="dynamic-nav"' in content:
        print(f"Skipping {file_path} - already processed.")
        return False
    
    # Skip non-html or specific system files
    if not file_path.endswith('.html') or 'test-sync-ok.html' in file_path:
        return False

    # 1. Inject CSS link in <head>
    if 'css/dropdown.css' not in content:
        css_link = '    <link rel="stylesheet" href="../css/dropdown.css">\n'
        content = re.sub(r'(<\/head>)', css_link + r'\1', content)

    # 2. Find and replace the MAIN navigation
    # We look for the first <nav> block that is NOT in <style>
    body_match = re.search(r'<body.*?>', content, re.IGNORECASE)
    if not body_match:
        print(f"Failed to find <body> in {file_path}")
        return False
    
    body_start = body_match.end()
    
    # Pattern to find the first <nav> block in the body
    nav_pattern = re.compile(r'<nav[\s\S]*?<\/nav>', re.IGNORECASE)
    
    # We find all navs in the whole content, but only replace the first one after body_start
    # To be safe, we split and join
    pre_body = content[:body_start]
    body_content = content[body_start:]
    
    dynamic_nav_html = '\n    <!-- Navigation -->\n    <nav class="navbar" id="dynamic-nav"></nav>\n    <script src="../js/navbar-component.js"></script>\n'
    
    new_body_content, count = nav_pattern.subn(dynamic_nav_html, body_content, count=1)
    
    if count > 0:
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(pre_body + new_body_content)
        print(f"Updated {file_path}")
        return True
    else:
        # If no <nav> found in body, maybe it's missing? Just print error
        print(f"Failed to find navbar in body of {file_path}")
        return False

# List of files to process
blog_dir = 'c:\\MyResumePortfolio\\blog'
pages_dir = 'c:\\MyResumePortfolio\\pages'

blog_files = [f for f in os.listdir(blog_dir) if f.endswith('.html')]
pages_files = [f for f in os.listdir(pages_dir) if f.endswith('.html')]

for f in blog_files:
    process_file(os.path.join(blog_dir, f))

for f in pages_files:
    process_file(os.path.join(pages_dir, f))
