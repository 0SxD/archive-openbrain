#!/usr/bin/env python3
import os
import json
import sys
import re
import argparse
from urllib.parse import urlparse

# Module 6 - Stage 2: The Research Airlock (Option C)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--target_file", required=True, help="File attempted to be written")
    parser.add_argument("--research_file", default="../research.md", help="Path to local research.md")
    parser.add_argument("--whitelist", default="../approved_sources.json", help="Path to approved_sources.json whitelist")
    return parser.parse_args()

def load_whitelist(json_path):
    # If the file doesn't exist yet, return default
    if not os.path.exists(json_path):
        return ["arxiv.org", "github.com", "docs.nautilustrader.io"]
    
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data.get("approved_domains", [])

def validate_write(target_file, research_file, whitelist):
    if not target_file.endswith(".py"):
        # Bypass gate for non-code files
        return True, ""
        
    if not os.path.exists(research_file):
        return False, f"[AIRLOCK BLOCK] No research.md found at {research_file}."
        
    with open(research_file, 'r', encoding='utf-8', errors='replace') as f:
        content = f.read()
        
    url_pattern = re.compile(r'https?://\S+')
    urls = url_pattern.findall(content)
    
    if not urls:
        return False, "[AIRLOCK BLOCK] No URL citations found in research.md."
        
    for url in urls:
        hostname = urlparse(url).hostname or ""
        for approved in whitelist:
            if hostname == approved or hostname.endswith('.' + approved):
                return True, f"Verified citation: {url}"
                
    return False, f"[AIRLOCK BLOCK] No citations from approved domains. Found: {urls}"

def main():
    args = parse_args()
    whitelist = load_whitelist(args.whitelist)
    
    passed, msg = validate_write(args.target_file, args.research_file, whitelist)
    
    if passed:
        print(f"PASS: {msg}")
        sys.exit(0)
    else:
        print(f"FAIL: {msg}\nYou must add a verified citation to research.md before writing Python code.")
        sys.exit(2)

if __name__ == "__main__":
    main()
