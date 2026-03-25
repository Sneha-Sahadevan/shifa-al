import os
import glob
from rembg import remove
from PIL import Image

def process_images():
    # Find all jpegs in assets subdirectories
    search_path = os.path.join("assets", "**", "*.jpg")
    for file_path in glob.glob(search_path, recursive=True):
        print(f"Processing: {file_path}")
        try:
            output_path = os.path.splitext(file_path)[0] + ".png"
            if os.path.exists(output_path):
                print(f"Skipping {file_path}, {output_path} already exists")
                continue
            
            input_image = Image.open(file_path)
            output_image = remove(input_image)
            output_image.save(output_path)
            print(f"Saved: {output_path}")
        except Exception as e:
            print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    process_images()
