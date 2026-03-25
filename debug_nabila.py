import cv2
import numpy as np
from PIL import Image
import os

# Configuration for standardization
TARGET_SIZE = (800, 1000)
FACE_SIZE_RATIO = 0.22
HEAD_TOP_MARGIN = 0.12

face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

def get_face_bbox(image_rgb):
    gray = cv2.cvtColor(image_rgb, cv2.COLOR_RGB2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    if len(faces) > 0:
        (x, y, w, h) = sorted(faces, key=lambda f: f[2]*f[3], reverse=True)[0]
        print(f"Face found: {x, y, w, h}")
        return {'x': float(x), 'y': float(y), 'w': float(w), 'h': float(h)}
    
    eyes = eye_cascade.detectMultiScale(gray, 1.1, 4)
    print(f"Eyes candidate count: {len(eyes)}")
    if len(eyes) >= 2:
        # Sort by y to find eyes that are likely a pair
        # Actually, just take the ones at the top of the person
        ex_min = min(e[0] for e in eyes)
        ey_min = min(e[1] for e in eyes)
        ex_max = max(e[0]+e[2] for e in eyes)
        ey_max = max(e[1]+e[3] for e in eyes)
        
        eye_w = ex_max - ex_min
        face_w = eye_w * 2.5
        face_h = face_w * 1.2
        face_x = ex_min - (face_w - eye_w) / 2
        face_y = ey_min - face_h * 0.3
        print(f"Estimated face from eyes: {face_x, face_y, face_w, face_h}")
        return {'x': float(face_x), 'y': float(face_y), 'w': float(face_w), 'h': float(face_h)}
    return None

def test_single():
    file_path = 'assets/Gynacology/Dr.Nabila Faisal.png'
    img_bgr = cv2.imread(file_path)
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    
    # Pre-resize (this matches the script)
    h, w = img_rgb.shape[:2]
    max_dim = 2000
    if h > max_dim or w > max_dim:
        scale = max_dim / max(h, w)
        img_rgb = cv2.resize(img_rgb, (int(w * scale), int(h * scale)), interpolation=cv2.INTER_AREA)

    face = get_face_bbox(img_rgb)
    if face:
        print(f"Final Detection: {face}")
    else:
        print("Detection FAILED")

if __name__ == "__main__":
    test_single()
