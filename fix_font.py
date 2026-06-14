import re
files = [r'c:\MyResumePortfolio\css\main.css', r'c:\MyResumePortfolio\css\premium.css', r'c:\MyResumePortfolio\css\premium.min.css']
for f in files:
    with open(f, 'r', encoding='utf-8') as file:
        content = file.read()
    
    # Replace block in unminified
    content = content.replace("font-family: 'Inter', sans-serif;\n      font-size: 1.15rem;\n      line-height: 1.9;", "font-family: 'Inter', sans-serif;\n      font-size: 1.15rem;\n      line-height: 1.9;\n      font-weight: 400;")
    
    # Replace block in minified
    content = content.replace("font-family:'Inter',sans-serif;font-size:1.15rem;line-height:1.9", "font-family:'Inter',sans-serif;font-size:1.15rem;line-height:1.9;font-weight:400")
    
    with open(f, 'w', encoding='utf-8') as file:
        file.write(content)
print('Done updating font-weight')
