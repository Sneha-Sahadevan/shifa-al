"""
Restores Dr. Thahseen Shah and Dr. Eman to their previous _standard.png
using the original standardize_photos.py settings.
"""
import os
from standardize_photos import standardize_image

IMAGES = [
    (r"assets\Gynacology\Dr.Thahseen Shah.jpg",
     r"assets\Gynacology\Dr.Thahseen Shah_standard.png"),
    (r"assets\Radiology\Dr.Eman.jpg",
     r"assets\Radiology\Dr.Eman_standard.png"),
]

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    for src, out in IMAGES:
        print(f"\nRestoring: {src}")
        standardize_image(src, out)
    print("\n=== Restored! ===")
