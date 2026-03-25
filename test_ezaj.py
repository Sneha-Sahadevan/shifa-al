import os
from standardize_photos import standardize_image

if __name__ == "__main__":
    img_path = r"c:\Users\SNEHA SAHADEVAN\OneDrive\Desktop\shifa al\assets\General Phsician\Dr.Ezaj.jpg"
    out_path = r"c:\Users\SNEHA SAHADEVAN\OneDrive\Desktop\shifa al\assets\General Phsician\Dr.Ezaj_standard.png"
    
    if os.path.exists(img_path):
        print(f"Testing standardization with NEW parameters on {img_path}")
        # Force overwrite by deleting if exists
        # Actually the script has a check but we can manually overwrite in test
        standardize_image(img_path, out_path)
        print(f"Result saved to {out_path}")
    else:
        print(f"Image not found at {img_path}")
