import os
import sys
from standardize_photos import standardize_image

if __name__ == "__main__":
    # Test on one image
    img_path = r"c:\Users\SNEHA SAHADEVAN\OneDrive\Desktop\shifa al\assets\General Phsician\Dr.Sherin Hameed.jpg"
    out_path = r"c:\Users\SNEHA SAHADEVAN\OneDrive\Desktop\shifa al\assets\General Phsician\Dr.Sherin Hameed_standard.png"
    
    if os.path.exists(img_path):
        print(f"Testing standardization on {img_path}")
        standardize_image(img_path, out_path)
        print(f"Result saved to {out_path}")
    else:
        print(f"Image not found at {img_path}")
