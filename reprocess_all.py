"""
Reprocesses all doctor images (including Dr. Arshiya Tabasssum)
using the updated standardize_photos.py that preserves original colors.

Run this from the 'shifa al' project folder:
    python reprocess_all.py
"""

import os
import glob
from standardize_photos import standardize_image

# Explicit list of images to regenerate (including missing ones)
FORCE_REGEN = [
    # Dr. Arshiya - no standard file exists yet
    r"assets\DENTAL\Dr.Arshiya Tabasssum.jpg",
]

def run():
    base_assets = "assets"
    subdirs = [f for f in os.listdir(base_assets) if os.path.isdir(os.path.join(base_assets, f))]

    processed = 0
    skipped = 0

    for subdir in subdirs:
        dir_path = os.path.join(base_assets, subdir)
        files = glob.glob(os.path.join(dir_path, "*.jpg")) + glob.glob(os.path.join(dir_path, "*.png"))

        for file_path in files:
            name = os.path.splitext(os.path.basename(file_path))[0]
            # Skip already-standardized files
            if name.endswith("_standard"):
                continue

            output_path = os.path.join(dir_path, f"{name}_standard.png")

            # Regenerate all (to remove old color filter)
            print(f"\n[Reprocessing] {file_path}")
            try:
                standardize_image(file_path, output_path)
                processed += 1
            except Exception as e:
                print(f"  FAILED: {e}")

    print(f"\n=== Done! Processed {processed} images. ===")

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    run()
