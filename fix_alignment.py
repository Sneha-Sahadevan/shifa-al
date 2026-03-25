import os
from standardize_photos import standardize_image

if __name__ == "__main__":
    # Fix Arshiya (Leaning)
    img_path = r"c:\Users\SNEHA SAHADEVAN\OneDrive\Desktop\shifa al\assets\DENTAL\Dr.Arshiya Tabasssum.jpg"
    out_path = r"c:\Users\SNEHA SAHADEVAN\OneDrive\Desktop\shifa al\assets\DENTAL\Dr.Arshiya Tabasssum_standard.png"
    
    if os.path.exists(img_path):
        print(f"Applying centering correction for Dr. Arshiya...")
        standardize_image(img_path, out_path)
        print(f"Result saved to {out_path}")
    else:
        print(f"Image not found at {img_path}")
