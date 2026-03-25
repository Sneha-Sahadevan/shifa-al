"""
Fix Dr. Thahseen Shah and Dr. Eman to match the head size/alignment of Dr. Khidr.
Uses body-mask-top anchor — no face detection — so head is always at consistent position.
"""

import os
import cv2
import numpy as np
from rembg import remove
from PIL import Image

TARGET_SIZE = (800, 1000)

# Match Dr. Khidr's look:
# head_region = how tall the head is as fraction of canvas height (bigger = more zoomed in)
# head_top_pad = fraction of canvas height above the top of the head
HEAD_REGION_RATIO = 0.26   # head height = 26% of canvas (Dr. Khidr reference)
HEAD_TOP_PAD      = 0.04   # 4% padding above head top

IMAGES = [
    {
        "src": r"assets\Gynacology\Dr.Thahseen Shah.jpg",
        "out": r"assets\Gynacology\Dr.Thahseen Shah_standard.png",
    },
    {
        "src": r"assets\Radiology\Dr.Eman.jpg",
        "out": r"assets\Radiology\Dr.Eman_standard.png",
    },
]

def process_image(file_path, output_path):
    print(f"\nLoading: {file_path}")
    img_bgr = cv2.imread(file_path)
    if img_bgr is None:
        print("  ERROR: Could not read image.")
        return
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    ih, iw = img_rgb.shape[:2]

    # Pre-resize large images
    max_dim = 2000
    if max(ih, iw) > max_dim:
        scale = max_dim / max(ih, iw)
        img_rgb = cv2.resize(img_rgb, (int(iw*scale), int(ih*scale)), interpolation=cv2.INTER_AREA)
        ih, iw = img_rgb.shape[:2]

    print("  Removing background...")
    pil_img  = Image.fromarray(img_rgb)
    nobg_pil = remove(pil_img, alpha_matting=True,
                      alpha_matting_foreground_threshold=240,
                      alpha_matting_background_threshold=10)
    nobg_np     = np.array(nobg_pil)
    mask        = nobg_np[:, :, 3]
    subject_rgb = nobg_np[:, :, :3]
    mask        = cv2.GaussianBlur(mask, (3, 3), 0)

    # Find subject bounding box
    y_coords, x_coords = np.where(mask > 10)
    if len(y_coords) == 0:
        print("  ERROR: No subject found.")
        return

    y_min   = int(np.min(y_coords))
    y_max   = int(np.max(y_coords))
    x_min   = int(np.min(x_coords))
    x_max   = int(np.max(x_coords))
    body_h  = y_max - y_min
    cx_body = (x_min + x_max) / 2.0

    print(f"  Subject: y={y_min}-{y_max}, x={x_min}-{x_max}, body_h={body_h}")

    # Head height estimated as top 18% of body height
    head_h_src    = body_h * 0.18
    target_head_h = TARGET_SIZE[1] * HEAD_REGION_RATIO
    scale_factor  = target_head_h / head_h_src

    new_w = int(iw * scale_factor)
    new_h = int(ih * scale_factor)

    # Build RGBA (original colours, no filter)
    processed_rgba = np.zeros((ih, iw, 4), dtype=np.uint8)
    processed_rgba[:, :, :3] = subject_rgb
    processed_rgba[:, :, 3]  = mask
    scaled = cv2.resize(processed_rgba, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)

    # Anchor points
    head_top_scaled = y_min * scale_factor
    cx_scaled       = cx_body * scale_factor

    target_head_top = TARGET_SIZE[1] * HEAD_TOP_PAD
    target_cx       = TARGET_SIZE[0] / 2.0

    offset_x = int(target_cx - cx_scaled)
    offset_y = int(target_head_top - head_top_scaled)

    print(f"  Scale: {scale_factor:.3f}, offset: ({offset_x}, {offset_y})")

    final_img  = Image.new("RGB", TARGET_SIZE, (255, 255, 255))
    scaled_pil = Image.fromarray(scaled)
    final_img.paste(scaled_pil, (offset_x, offset_y), scaled_pil)
    final_img.save(output_path, "PNG")
    print(f"  Saved: {output_path}")


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for entry in IMAGES:
        process_image(entry["src"], entry["out"])
    print("\n=== Done! ===")
