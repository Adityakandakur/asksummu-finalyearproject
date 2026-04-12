import re
import os

# Read the file
with open('t.html', 'r', encoding='utf-8') as f:
    content = f.read()

# More aggressive minification
# Remove all newlines outside of strings
lines = content.split('\n')
cleaned_lines = []
for line in lines:
    # Skip empty lines
    stripped = line.strip()
    if stripped and not stripped.startswith('//'):
        cleaned_lines.append(stripped)

content = ''.join(cleaned_lines)

# Compress consecutive spaces (but preserve single space where needed)
content = re.sub(r'  +', ' ', content)

# Remove space before closing tags
content = re.sub(r' >', '>', content)

# Remove space after opening tags in most cases
content = re.sub(r'> ', '>', content)

# Remove spaces around = in attributes
content = re.sub(r'\s*=\s*', '=', content)

# Minify data carefully
content = re.sub(r"'data-", "'data-", content)

# Write minified version
with open('t.html', 'w', encoding='utf-8') as f:
    f.write(content)

# Get new size
new_size = os.path.getsize('t.html')
print(f"Minified: {new_size} bytes ({new_size/1024:.1f}KB)")
print(f"Compression achieved!")
