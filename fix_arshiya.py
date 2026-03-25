import os
import cv2
import numpy as np
from standardize_photos import standardize_image
import standardize_photos

if __name__ == "__main__":
    img_path = r"c:\Users\SNEHA SAHADEVAN\OneDrive\Desktop\shifa al\assets\DENTAL\Dr.Arshiya Tabasssum.jpg"
    out_path = r"c:\Users\SNEHA SAHADEVAN\OneDrive\Desktop\shifa al\assets\DENTAL\Dr.Arshiya Tabasssum_standard.png"
    
    if os.path.exists(img_path):
        print(f"Fixing Dr. Arshiya's head level...")
        # Temporarily increase margins and decrease face size for better headroom
        old_ratio = standardize_photos.FACE_SIZE_RATIO
        old_margin = standardize_photos.HEAD_TOP_MARGIN
        
        standardize_photos.FACE_SIZE_RATIO = 0.20 # Zoom out more
        standardize_photos.HEAD_TOP_MARGIN = 0.25 # More headroom
        
        standardize_image(img_path, out_path)
        
        # Restore
        standardize_photos.FACE_SIZE_RATIO = old_ratio
        standardize_photos.HEAD_TOP_MARGIN = old_margin
        
        print(f"Result saved to {out_path}")
    else:
        print(f"Image not found at {img_path}")
