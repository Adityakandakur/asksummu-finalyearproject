#!/usr/bin/env python3
import re
import os

def aggressive_minify(filepath):
    """More aggressive minification"""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_size = len(content.encode('utf-8'))
    
    # Minify CSS more aggressively
    def minify_heavy_css(match):
        css = match.group(1)
        # Remove all whitespace except where syntactically needed
        css = re.sub(r'\s+', ' ', css)
        css = re.sub(r'\s*([{}:;,()])\s*', r'\1', css)
        css = re.sub(r':(?=[^ ])', ':', css)  # Remove spaces properly
        return '<style>' + css.strip() + '</style>'
    
    content = re.sub(r'<style>([\s\S]*?)</style>', minify_heavy_css, content)
    
    # Aggressively minify inline styles
    def minify_inline_style(match):
        style_val = match.group(1)
        style_val = re.sub(r'\s*([{}:;,()])\s*', r'\1', style_val)
        style_val = re.sub(r':(?!\w)', ':', style_val)  # Remove space after :
        return f'style="{style_val}"'
    
    content = re.sub(r'style="([^"]*)"', minify_inline_style, content)
    
    # Compress common patterns
    content = re.sub(r'\s+', ' ', content)  # All multiple whitespace to single
    content = re.sub(r'>\s+<', '><', content)  # No space between tags
    content = re.sub(r'\s*=\s*', '=', content)  # No spaces around =
    content = re.sub(r'\s+(/?)>', r'\1>', content)  # No space before > or />
    content = re.sub(r'<\s+', '<', content)  # No space after <
    
    # Remove spaces in common HTML patterns
    content = re.sub(r'<!--[\s\S]*?-->', '', content)  # Comments
    content = re.sub(r'\s+', ' ', content)  # Normalize spaces again
    
    minified_size = len(content.encode('utf-8'))
    compression = round((1 - minified_size / original_size) * 100, 1)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"\n📦 Compression Summary:")
    print(f"  Original Size:  {original_size:,} bytes ({original_size/1024:.1f}KB)")
    print(f"  Minified Size:  {minified_size:,} bytes ({minified_size/1024:.1f}KB)")
    print(f"  Compression:    {compression}%")
    print(f"  Size Reduced:   {(original_size-minified_size):,} bytes\n")

if __name__ == '__main__':
    aggressive_minify('/Users/adityakandakur/Desktop/finalt/t.html')
