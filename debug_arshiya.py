import cv2
import numpy as np
import os
import standardize_photos
from rembg import remove
from PIL import Image

def debug_arshiya():
    path = r"c:\Users\SNEHA SAHADEVAN\OneDrive\Desktop\shifa al\assets\DENTAL\Dr.Arshiya Tabasssum.jpg"
    img_bgr = cv2.imread(path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    # Get mask
    pil_img = Image.fromarray(img_rgb)
    nobg_pil = remove(pil_img)
    nobg_np = np.array(nobg_pil)
    
    print(f"Original shape: {img_rgb.shape}")
    print(f"Rembg shape: {nobg_np.shape}")
    
    mask = nobg_np[:, :, 3]
    face = standardize_photos.get_face_bbox(img_rgb, mask=mask)
    print(f"Face bbox: {face}")

if __name__ == "__main__":
    debug_arshiya()
