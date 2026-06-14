import os
import re

def update_html_references(root_dir):
    # Regex to find image src attributes
    # Supports both absolute-ish (relative to project root) and relative paths
    img_regex = re.compile(r'src=["\']([^"\']+\.(?:png|jpg|jpeg))["\']', re.IGNORECASE)
    
    html_count = 0
    ref_count = 0

    print(f"Scanning for HTML files in {root_dir}...")

    for subdir, _, files in os.walk(root_dir):
        # Skip directories
        if any(ignored in subdir for ignored in ['.git', 'node_modules', '.terraform', '.agent', 'scripts']):
            continue

        for file in files:
            if file.lower().endswith('.html'):
                file_path = os.path.join(subdir, file)
                modified = False
                
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                def replace_match(match):
                    nonlocal modified, ref_count
                    original_src = match.group(1)
                    
                    # Construct potential webp path relative to the HTML file
                    webp_src = os.path.splitext(original_src)[0] + '.webp'
                    
                    # Check if the webp file actually exists locally
                    # The src is relative to the HTML file location
                    potential_webp_local = os.path.normpath(os.path.join(subdir, webp_src))
                    
                    if os.path.exists(potential_webp_local):
                        ref_count += 1
                        modified = True
                        # Return the full matched string with replaced extension
                        return match.group(0).replace(original_src, webp_src)
                    
                    return match.group(0)

                new_content = img_regex.sub(replace_match, content)

                if modified:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    html_count += 1
                    print(f"Updated: {file} ({file_path})")

    print(f"\nUpdate Summary:")
    print(f"HTML Files Modified: {html_count}")
    print(f"Image References Switched to WebP: {ref_count}")

if __name__ == "__main__":
    # Get project root (parent of scripts/)
    project_root = os.path.dirname(os.path.dirname(__file__))
    update_html_references(project_root)
