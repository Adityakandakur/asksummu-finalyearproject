#!/usr/bin/env python3
import re
import os

def ultra_minify(filepath):
    """Ultra-aggressive minification targeting JS and data"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_size = len(content.encode('utf-8'))
    
    # 1. Remove HTML comments completely
    content = re.sub(r'<!--[\s\S]*?-->', '', content)
    
    # 2. Remove extra spaces and newlines everywhere
    content = re.sub(r'[\r\n]+', ' ', content)
    
    # 3. Compress multiple spaces
    content = re.sub(r' {2,}', ' ', content)
    
    # 4. Process style tags - AGGRESSIVE
    def minify_style(match):
        css = match.group(1)
        css = re.sub(r'\s+', ' ', css)  # Collapse whitespace
        css = re.sub(r'\s*([{};:,])\s*', r'\1', css)  # No spaces around delimiters
        css = re.sub(r':\s+', ':', css)  # 0 space after colons
        css = re.sub(r';\s*}', '}', css)  # Remove; before }
        return '<style>' + css + '</style>'
    
    content = re.sub(r'<style[^>]*>([\s\S]*?)</style>', minify_style, content)
    
    # 5. Minify inline style attributes more aggressively
    def minify_inline(match):
        s = match.group(1)
        s = re.sub(r'\s+', '', s)  # Remove ALL spaces in style attribute
        s = re.sub(r':\s*', ':', s)
        s = re.sub(r';\s*', ';', s)
        return f'style="{s}"'
    
    content = re.sub(r'style="([^"]*)"', minify_inline, content)
    
    # 6. Remove spaces between tags
    content = re.sub(r'>\s*<', '><', content)
    
    # 7. Minify attributes
    content = re.sub(r'\s*=\s*', '=', content)
    
    # 8. Compress data-* attributes
    content = re.sub(r'data-(\w+)="([^"]*)"', lambda m: f'data-{m.group(1)}="{m.group(2).strip()}"', content)
    
    # 9. Remove spaces before /> and >
    content = re.sub(r'\s+(/?>)', r'\1', content)
    
    # 10. Final whitespace cleanup but keep structural spaces
    content = re.sub(r'\s{2,}', ' ', content)
    
    minified_size = len(content.encode('utf-8'))
    compression = round((1 - minified_size / original_size) * 100, 1)
    saved = original_size - minified_size
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n═══════════════════════════════════════")
    print(f"  📦 HTML COMPRESSION COMPLETE 📦")
    print(f"═══════════════════════════════════════")
    print(f"  Original Size:  {original_size:,} bytes ({original_size/1024:.2f}KB)")
    print(f"  Minified Size:  {minified_size:,} bytes ({minified_size/1024:.2f}KB)")
    print(f"  ───────────────────────────────────")
    print(f"  Compression:    {compression}%")
    print(f"  Size Reduced:   {saved:,} bytes")
    print(f"═══════════════════════════════════════\n")

if __name__ == '__main__':
    ultra_minify('/Users/adityakandakur/Desktop/finalt/t.html')
