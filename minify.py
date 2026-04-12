import re
import os

# Read the file
with open('t.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Minify comments - remove HTML comments
content = re.sub(r'<!--.*?-->', '', content, flags=re.DOTALL)

# Minify CSS - preserve essential formatting
def minify_style(match):
    style_content = match.group(1)
    # Remove newlines and excessive spaces
    style_content = re.sub(r'\n', '', style_content)
    style_content = re.sub(r'\s+', ' ', style_content)
    style_content = re.sub(r':\s+', ':', style_content)
    style_content = re.sub(r';\s*', ';', style_content)
    style_content = re.sub(r'{\s*', '{', style_content)
    style_content = re.sub(r'\s*}', '}', style_content)
    style_content = re.sub(r',\s+', ',', style_content)
    # Remove spaces around operators in CSS
    style_content = re.sub(r'\s*\(\s*', '(', style_content)
    style_content = re.sub(r'\s*\)\s*', ')', style_content)
    return f'<style>{style_content.strip()}</style>'

content = re.sub(r'<style[^>]*>(.*?)</style>', minify_style, content, flags=re.DOTALL)

# Remove excessive whitespace between tags
content = re.sub(r'>\s+<', '><', content)

# Minify inline styles 
content = re.sub(r'style="([^"]*)"', lambda m: f'style="{re.sub(r"\\s+", "", m.group(1)).replace(": ", ":").replace("; ", ";")}"', content)

# Write minified version
with open('t.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Calculate new size
new_size = os.path.getsize('t.html')
print(f"Minified file: {new_size} bytes ({new_size/1024:.1f}KB)")
