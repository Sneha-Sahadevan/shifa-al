import os
import glob
import cv2
import numpy as np
from rembg import remove
from PIL import Image

# Configuration for standardization
TARGET_SIZE = (800, 1000)  # Width, Height (4:5)
FACE_SIZE_RATIO = 0.22  # Face should be roughly 22% of image height (Zoomed out more)
HEAD_TOP_MARGIN = 0.08  # Less space above head (8% of image height, aligning heads high like Dr. Nazeer)

# Load Haar Cascades
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
# Add eye cascade for Niqab/Mask detection
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def get_face_bbox(image_rgb, mask=None):
    # Haar Cascade works better on grayscale
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    
    if mask is not None:
        # Ignore parts of the image that aren't the subject
        # Use a soft mask (binary)
        _, binary = cv2.threshold(mask, 10, 255, cv2.THRESH_BINARY)
        gray = cv2.bitwise_and(gray, gray, mask=binary)
    
    # Try face first with stricter parameters
    faces = face_cascade.detectMultiScale(gray, 1.1, 5, minSize=(100, 100))
    if len(faces) > 0:
        (x, y, w, h) = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)[0]
        return {'x': float(x), 'y': float(y), 'w': float(w), 'h': float(h)}
    
    # Try eyes if face fails (good for Niqab)
    # Search for eyes in top half of the person
    eyes = eye_cascade.detectMultiScale(gray, 1.1, 6)
    if len(eyes) >= 2:
        # Group eyes that relate to each other
        # Candidates should be in the top portion of the mask
        valid_eyes = []
        if mask is not None:
            y_coords, _ = np.where(mask > 0)
            if len(y_coords) > 0:
                y_min = np.min(y_coords)
                y_max = np.max(y_coords)
                # Keep eyes in the top 35% of the person
                y_threshold = y_min + (y_max - y_min) * 0.35
                valid_eyes = [e for e in eyes if e[1] < y_threshold]
        else:
            valid_eyes = list(eyes)

        if len(valid_eyes) >= 2:
            ex_min = min(e[0] for e in valid_eyes)
            ey_min = min(e[1] for e in valid_eyes)
            ex_max = max(e[0]+e[2] for e in valid_eyes)
            ey_max = max(e[1]+e[3] for e in valid_eyes)
            
            eye_w = ex_max - ex_min
            # Sanity check: face width shouldn't be crazy
            if eye_w < image_rgb.shape[1] * 0.4:
                face_w = eye_w * 2.5
                face_h = face_w * 1.2
                face_x = ex_min - (face_w - eye_w) / 2
                face_y = ey_min - face_h * 0.3
                return {'x': float(face_x), 'y': float(face_y), 'w': float(face_w), 'h': float(face_h)}

    return None

def adjust_lighting(image_np, mask):
    """No-op: return image as-is to preserve original colors."""
    return image_np

def standardize_image(file_path, output_path):
    print(f"Processing: {file_path}")
    
    # Load image
    img_bgr = cv2.imread(file_path)
    if img_bgr is None:
        print(f"  Error: Could not read {file_path}")
        return
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    ih, iw, _ = img_rgb.shape
    
    # Pre-resize if image is massive (to save memory in rembg)
    h, w = img_rgb.shape[:2]
    max_dim = 2000
    if h > max_dim or w > max_dim:
        scale = max_dim / max(h, w)
        img_rgb = cv2.resize(img_rgb, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)
        ih, iw = img_rgb.shape[:2] # Update dimensions

    # 1. Remove Background first to get subject mask with alpha matting for cleaner edges
    print("  Removing background...")
    pil_img = Image.fromarray(img_rgb)
    # Using alpha matting for higher quality edges
    nobg_pil = remove(pil_img, alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=10)
    nobg_np = np.array(nobg_pil)
    
    mask = nobg_np[:, :, 3]
    subject_rgb = nobg_np[:, :, :3]
    
    # Smooth the mask to remove jagged edges
    mask = cv2.GaussianBlur(mask, (3, 3), 0)
    
    # 2. Detect Face or Fallback
    # Pass mask to filter detections to only the subject
    face = get_face_bbox(img_rgb, mask=mask)
    if not face:
        print("  Warning: No face detected. Using subject mask fallback.")
        y_coords, x_coords = np.where(mask > 0)
        if len(y_coords) > 0:
            y_min, y_max = np.min(y_coords), np.max(y_coords)
            x_min, x_max = np.min(x_coords), np.max(x_coords)
            # Estimate face position at the top 1/6th of the subject
            # Estimate face position at the top of the subject
            # Use 15% of body height as head size
            face_h = (y_max - y_min) * 0.15
            # Center horizontally in the subject's mask, and put the top lower down
            face = {'x': (x_min + x_max)/2 - face_h/2, 'y': y_min + (y_max-y_min)*0.10, 'w': face_h, 'h': face_h}
        else:
            face = {'x': iw/4, 'y': ih/10, 'w': iw/2, 'h': ih/4}

    # 3. Keep original colors — no lighting/tint adjustment
    print("  Keeping original colors (no filter applied)...")
    
    # Re-combine with mask
    processed_rgba = np.zeros((ih, iw, 4), dtype=np.uint8)
    processed_rgba[:, :, :3] = subject_rgb
    processed_rgba[:, :, 3] = mask
    
    # 4. Reframing Logic
    target_face_h = TARGET_SIZE[1] * FACE_SIZE_RATIO
    scale_factor = target_face_h / face['h']
    
    new_w = int(iw * scale_factor)
    new_h = int(ih * scale_factor)
    
    scaled_subject = cv2.resize(processed_rgba, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
    
    # Calculate crop center horizontally
    fcx_scaled = (face['x'] + face['w'] / 2) * scale_factor
    target_fcx = TARGET_SIZE[0] / 2
    
    # Custom correction for Dr. Arshiya's leaning pose
    if "Arshiya" in output_path:
        target_fcx += 60 # Shift right by 60px
        
    # --- ABSOLUTE HEAD LEVEL ANCHORING ---
    # Find the top of the person's body mask natively
    y_coords, x_coords = np.where(mask > 0)
    if len(y_coords) > 0:
        y_min_native = np.min(y_coords)
    else:
        y_min_native = face['y']
        
    head_top_scaled = y_min_native * scale_factor
    target_head_top = HEAD_TOP_MARGIN * TARGET_SIZE[1]
    
    offset_x = int(target_fcx - fcx_scaled)
    # Always align the top of the head exactly to the target head top margin!
    offset_y = int(target_head_top - head_top_scaled)
    
    # Final composite on white background
    final_img = Image.new("RGB", TARGET_SIZE, (255, 255, 255))
    
    scaled_subject_pil = Image.fromarray(scaled_subject)
    final_img.paste(scaled_subject_pil, (offset_x, offset_y), scaled_subject_pil)
    
    # 5. Save output
    final_img.save(output_path, "PNG", quality=95)
    print(f"  Saved to: {output_path}")

def run():
    base_assets = "assets"
    subdirs = [f for f in os.listdir(base_assets) if os.path.isdir(os.path.join(base_assets, f))]
    
    for subdir in subdirs:
        dir_path = os.path.join(base_assets, subdir)
        # Process both jpg and png files
        files = glob.glob(os.path.join(dir_path, "*.jpg")) + glob.glob(os.path.join(dir_path, "*.png"))
        for file_path in files:
            name = os.path.splitext(os.path.basename(file_path))[0]
            # Skip standard files and temporary results
            if name.endswith("_standard"): continue
            
            output_path = os.path.join(dir_path, f"{name}_standard.png")
            # if os.path.exists(output_path): continue
                 
            try:
                standardize_image(file_path, output_path)
            except Exception as e:
                print(f"Failed to process {file_path}: {e}")

if __name__ == "__main__":
    run()
