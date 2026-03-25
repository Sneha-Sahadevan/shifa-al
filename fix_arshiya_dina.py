import os
import cv2
import numpy as np
import standardize_photos
from standardize_photos import standardize_image

def process_custom(name, folder, ratio, top, x_shift=0):
    path = os.path.join("assets", folder, f"{name}.jpg")
    out = os.path.join("assets", folder, f"{name}_standard.png")
    
    if os.path.exists(path):
        print(f"Standardizing {name} with ratio={ratio}, top={top}, x_shift={x_shift}")
        # We need to monkey-patch or modify the standardize_image locally
        # Since I can't easily modify the function internals without copying it,
        # I'll just write a custom version here or use global offsets if I can add them to the script.
        
        # Actually, I'll just modify standardize_photos.py once to accept an extra shift, 
        # but for now I'll just use a quick fix in this script by re-pasting.
        
        # Re-running with current script logic which now has better headroom.
        old_ratio = standardize_photos.FACE_SIZE_RATIO
        old_top = standardize_photos.HEAD_TOP_MARGIN
        
        standardize_photos.FACE_SIZE_RATIO = ratio
        standardize_photos.HEAD_TOP_MARGIN = top
        
        # We'll manually adjust the offset if needed by modifying the paste logic or just shifting the output file
        # But wait! I can just use the debug image logic to see.
        
        # I'll modify standardize_photos.py to handle a horizontal shift if I see an environment variable or something?
        # No, I'll just fix Arshiya by adjusting her face_x in a wrapper.
        
        # Let's try this: shift her face_center in the original.
        ih, iw = cv2.imread(path).shape[:2]
        img_rgb = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
        
        # Get face from script logic
        from PIL import Image
        from rembg import remove
        mask = np.array(remove(Image.fromarray(img_rgb)))[:,:,3]
        face = standardize_photos.get_face_bbox(img_rgb, mask=mask)
        
        if not face:
             # Fallback
             y_coords, x_coords = np.where(mask > 0)
             y_min, y_max = np.min(y_coords), np.max(y_coords)
             x_min, x_max = np.min(x_coords), np.max(x_coords)
             face_h = (y_max - y_min) * 0.15
             face = {'x': (x_min + x_max)/2 - face_h/2, 'y': y_min + (y_max-y_min)*0.10, 'w': face_h, 'h': face_h}
        
        # Shift face to the LEFT to move person to the RIGHT
        face['x'] -= x_shift / (ratio * 1000 / face['h']) # approx conversion
        
        # Now call the logic manually
        # (I'll just use my previous fix_arshiya_dina.py logic)
        standardize_image(path, out)
        
        # Finish
        standardize_photos.FACE_SIZE_RATIO = old_ratio
        standardize_photos.HEAD_TOP_MARGIN = old_top
    else:
        print(f"Skipping {name}, source not found at {path}")

if __name__ == "__main__":
    # Arshiya: ratio 0.22, top 0.30 worked for headroom.
    # Now she is too far LEFT. We need to shift her facial center more to the LEFT in original? 
    # Wait! If face center is at X=100 and we want it at X=200, we move person right.
    # My previous logic: face['x'] -= ... will move her body RIGHT.
    
    # I'll use a better approach: I'll update standardize_photos.py to center everything properly first.
    pass
