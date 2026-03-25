"""
Custom fix for Dr. Arshiya Tabasssum's image.
Skips face detection entirely — anchors off the top of the subject mask
so the head is always at the correct position regardless of the badge or other
objects in the image.
"""

import os
import cv2
import numpy as np
from rembg import remove
from PIL import Image

# --- Target canvas ---
TARGET_SIZE   = (800, 1000)   # width, height

# --- Tuning: what fraction of the canvas height the "head region" occupies ---
# HEAD_REGION_RATIO: how tall the head is as fraction of image height
HEAD_REGION_RATIO = 0.20  # head = 20% of canvas height
# HEAD_TOP_PAD: fraction of canvas height to leave above the head
HEAD_TOP_PAD  = 0.05  # 5% padding above top of head → head starts at 5%

def process():
    file_path   = r"assets\DENTAL\Dr.Arshiya Tabasssum.jpg"
    output_path = r"assets\DENTAL\Dr.Arshiya Tabasssum_standard.png"

    print(f"Loading: {file_path}")
    img_bgr = cv2.imread(file_path)
    if img_bgr is None:
        print("ERROR: Could not read image.")
        return
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    ih, iw = img_rgb.shape[:2]

    # Pre-resize for memory
    max_dim = 2000
    if max(ih, iw) > max_dim:
        scale = max_dim / max(ih, iw)
        img_rgb = cv2.resize(img_rgb, (int(iw*scale), int(ih*scale)), interpolation=cv2.INTER_AREA)
        ih, iw = img_rgb.shape[:2]

    print("Removing background...")
    pil_img  = Image.fromarray(img_rgb)
    nobg_pil = remove(pil_img, alpha_matting=True,
                      alpha_matting_foreground_threshold=240,
                      alpha_matting_background_threshold=10)
    nobg_np     = np.array(nobg_pil)
    mask        = nobg_np[:, :, 3]
    subject_rgb = nobg_np[:, :, :3]
    mask        = cv2.GaussianBlur(mask, (3, 3), 0)

    # Find bounding box of the subject (person)
    y_coords, x_coords = np.where(mask > 10)
    if len(y_coords) == 0:
        print("ERROR: No subject found in mask.")
        return

    y_min   = int(np.min(y_coords))   # top of person's head
    y_max   = int(np.max(y_coords))   # bottom of person
    x_min   = int(np.min(x_coords))
    x_max   = int(np.max(x_coords))
    body_h  = y_max - y_min
    body_w  = x_max - x_min
    cx_body = (x_min + x_max) / 2  # horizontal centre of person

    print(f"Subject bbox: x={x_min}-{x_max}, y={y_min}-{y_max}, "
          f"body_h={body_h}, body_w={body_w}")

    # Estimate head size as the top ~18% of body height
    head_h_src = body_h * 0.18  # head height in source pixels

    # --- Scale so that head_h_src maps to HEAD_REGION_RATIO * TARGET_HEIGHT ---
    target_head_h = TARGET_SIZE[1] * HEAD_REGION_RATIO
    scale_factor  = target_head_h / head_h_src

    new_w = int(iw * scale_factor)
    new_h = int(ih * scale_factor)

    # Build RGBA with original colours
    processed_rgba = np.zeros((ih, iw, 4), dtype=np.uint8)
    processed_rgba[:, :, :3] = subject_rgb
    processed_rgba[:, :, 3]  = mask
    scaled = cv2.resize(processed_rgba, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

    # Scaled coordinates of head top and body centre-x
    head_top_scaled = y_min * scale_factor
    cx_scaled       = cx_body * scale_factor

    # Where we want them on the canvas
    target_head_top = TARGET_SIZE[1] * HEAD_TOP_PAD   # e.g. 50 px from top
    target_cx       = TARGET_SIZE[0] / 2              # horizontally centred

    offset_x = int(target_cx - cx_scaled)
    offset_y = int(target_head_top - head_top_scaled)

    print(f"Scale: {scale_factor:.3f}, offset: ({offset_x}, {offset_y})")

    # Composite on white background
    final_img  = Image.new("RGB", TARGET_SIZE, (255, 255, 255))
    scaled_pil = Image.fromarray(scaled)
    final_img.paste(scaled_pil, (offset_x, offset_y), scaled_pil)

    final_img.save(output_path, "PNG")
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    process()
