import re
import os

def update_doctors_html():
    file_path = "doctors.html"
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
        
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # regex to find img tags within practitioner-cards and change src to standard version
    # find: src="./assets/DENTAL/Dr.Kazmeen Afroz (Orthodontist).jpg"
    # replace with: src="./assets/DENTAL/Dr.Kazmeen Afroz (Orthodontist)_standard.png"
    
    # We want to match src attributes that point to assets and end in png or jpg
    # But only if they haven't been standardized yet.
    def replace_src(match):
        original_src = match.group(1)
        if "_standard.png" in original_src:
            return f'src="{original_src}"'
        
        # split into path and ext
        base, ext = os.path.splitext(original_src)
        # remove existing _standard if any (shouldn't be there given the if above)
        if base.endswith("_standard"):
             return f'src="{base}.png"'
             
        new_src = f"{base}_standard.png"
        return f'src="{new_src}"'

    # Match src="./assets/..." or src="assets/..."
    new_content = re.sub(r'src="(.*assets\/.*?\.(?:jpg|png))"', replace_src, content)
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print("Updated doctors.html image sources.")

if __name__ == "__main__":
    update_doctors_html()
