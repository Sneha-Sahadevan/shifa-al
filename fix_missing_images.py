import os
import re
from difflib import get_close_matches

def find_mismatches():
    # 1. Map all files in assets
    asset_files = {}
    for root, dirs, files in os.walk("assets"):
        for f in files:
            if not f.endswith("_standard.png"): # Only original files for matching
                # Store full path indexed by filename (no ext)
                name_key = os.path.splitext(f)[0].lower()
                asset_files[name_key] = os.path.join(root, f)

    # 2. Parse doctors.html
    with open("doctors.html", "r", encoding="utf-8") as f:
        html = f.read()

    # Find cards
    cards = re.findall(r'<div class="practitioner-card">.*?<img src="(.*?)".*?<h3 class="practitioner-name">(.*?)</h3>', html, re.DOTALL)
    
    print(f"Checking {len(cards)} doctors...")
    updates = []
    for src, name in cards:
        full_path = src.replace("./", "")
        if os.path.exists(full_path):
            # print(f"OK: {name} -> {src}")
            pass
        else:
            print(f"MISSING: {name} (tried {src})")
            # Try to find a match
            clean_name = name.lower().replace("dr. ", "").strip()
            # Search in our mapped asset files
            keys = list(asset_files.keys())
            matches = get_close_matches(clean_name, keys, n=1, cutoff=0.3)
            
            if not matches:
                 # try original file keys
                 matches = get_close_matches(name.lower(), keys, n=1, cutoff=0.3)

            if matches:
                matching_file = asset_files[matches[0]]
                print(f"  FOUND POTENTIAL MATCH: {matching_file}")
                # We want to use the standard version of this file
                base, ext = os.path.splitext(matching_file)
                new_src = f"./{base}_standard.png".replace("\\", "/")
                updates.append((src, new_src))
            else:
                print(f"  NO MATCH FOUND FOR {name}")

    if updates:
        print(f"\nFound {len(updates)} updates. Applying...")
        for old, new in updates:
            html = html.replace(old, new)
        
        with open("doctors.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("Updated doctors.html")
    else:
        print("No matches found to update.")

if __name__ == "__main__":
    find_mismatches()
