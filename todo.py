import os
import re

def list_todo():
    with open("doctors.html", "r", encoding="utf-8") as f:
        html = f.read()

    cards = re.findall(r'<div class="practitioner-card">.*?<img src="(.*?)".*?<h3 class="practitioner-name">(.*?)</h3>', html, re.DOTALL)
    
    print("Checking which images are missing...")
    todo = []
    for src, name in cards:
        full_path = src.replace("./", "")
        if not os.path.exists(full_path):
            print(f"MISSING: {name} ({src})")
            todo.append(name)
            
    if not todo:
        print("All images found!")
    else:
        print(f"\n{len(todo)} images are yet to be generated.")

if __name__ == "__main__":
    list_todo()
