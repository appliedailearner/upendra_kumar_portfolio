
import re

def check_balance(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    # Find all <div> and </div> tags
    div_opens = re.findall(r'<div[\s>]', content)
    div_closes = re.findall(r'</div>', content)
    
    # Find all <article and </article tags
    article_opens = re.findall(r'<article[\s>]', content)
    article_closes = re.findall(r'</article>', content)

    # Find all <aside and </aside tags
    aside_opens = re.findall(r'<aside[\s>]', content)
    aside_closes = re.findall(r'</aside>', content)

    print(f"File: {filename}")
    print(f"DIVs: {len(div_opens)} open, {len(div_closes)} close. Balance: {len(div_opens) - len(div_closes)}")
    print(f"ARTICLEs: {len(article_opens)} open, {len(article_closes)} close. Balance: {len(article_opens) - len(article_closes)}")
    print(f"ASIDEs: {len(aside_opens)} open, {len(aside_closes)} close. Balance: {len(aside_opens) - len(aside_closes)}")

    # Specific check for exec-summary-container
    summary_count = content.count('exec-summary-container')
    print(f"exec-summary-container occurrences: {summary_count}")

check_balance('C:/MyResumePortfolio/blog/2026-02-01-azure-landing-zone-network-observability.html')
