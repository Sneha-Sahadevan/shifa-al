import os
import glob

def find_unprocessed():
    assets = "assets"
    subdirs = [f for f in os.listdir(assets) if os.path.isdir(os.path.join(assets, f))]
    
    unprocessed = []
    for d in subdirs:
        dir_path = os.path.join(assets, d)
        files = glob.glob(os.path.join(dir_path, "*.jpg")) + glob.glob(os.path.join(dir_path, "*.png"))
        for f in files:
            name = os.path.splitext(os.path.basename(f))[0]
            if name.endswith("_standard"): continue
            
            standard = os.path.join(dir_path, f"{name}_standard.png")
            if not os.path.exists(standard):
                unprocessed.append(f)
    
    print(f"Found {len(unprocessed)} unprocessed files:")
    for f in unprocessed:
        print(f" - {f}")
        
if __name__ == "__main__":
    find_unprocessed()
