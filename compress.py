#!/usr/bin/env python3
import re
import os
import sys

def minify_html(filepath):
    """Minify HTML file while preserving functionality"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_size = len(content.encode('utf-8'))
    
    # 1. Remove HTML comments
    content = re.sub(r'<!--[\s\S]*?-->', '', content)
    
    # 2. Remove extra newlines and tabs
    content = re.sub(r'[\r\n\t]+', ' ', content)
    
    # 3. Remove multiple spaces (but be careful with string content)
    content = re.sub(r' {2,}', ' ', content)
    
    # 4. Remove space around equals in attributes
    content = re.sub(r'\s*=\s*', '=', content)
    
    # 5. Remove spaces between tags
    content = re.sub(r'>\s+<', '><', content)
    
    # 6. Minify style attribute values
    def minify_style_attr(match):
        attr = match.group(0)
        # Remove spaces after colons and semicolons in style
        attr = re.sub(r':\s+', ':', attr)
        attr = re.sub(r';\s+', ';', attr)
        attr = re.sub(r',\s+', ',', attr)
        return attr
    
    content = re.sub(r'style="[^"]*"', minify_style_attr, content)
    
    # 7. Remove unnecessary spaces before > and />
    content = re.sub(r'\s+(/?>)', r'\1', content)
    
    # 8. Minify inline styles in style tag (without breaking functionality)
    def minify_css(match):
        css = match.group(1)
        # Remove newlines
        css = re.sub(r'\n', '', css)
        # Remove spaces around CSS syntax chars
        css = re.sub(r':\s*', ':', css)
        css = re.sub(r';\s*', ';', css)
        css = re.sub(r',\s+', ',', css)
        css = re.sub(r'{\s*', '{', css)
        css = re.sub(r'\s*}', '}', css)
        css = re.sub(r'\(\s*', '(', css)
        css = re.sub(r'\s*\)', ')', css)
        css = re.sub(r'  +', ' ', css)
        return '<style>' + css.strip() + '</style>'
    
    content = re.sub(r'<style>([\s\S]*?)</style>', minify_css, content)
    
    # 9. Clean up remaining excess spaces
    content = re.sub(r'\s{2,}', ' ', content)
    
    minified_size = len(content.encode('utf-8'))
    compression = round((1 - minified_size / original_size) * 100, 1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✓ Original: {original_size:,} bytes ({original_size/1024:.1f}KB)")
    print(f"✓ Minified: {minified_size:,} bytes ({minified_size/1024:.1f}KB)")
    print(f"✓ Compression: {compression}%")
    print(f"✓ Saved: {original_size - minified_size:,} bytes")

if __name__ == '__main__':
    filepath = '/Users/adityakandakur/Desktop/finalt/t.html'
    minify_html(filepath)
