import os
from PIL import Image

def generate_favicons():
    logo_path = "assets/transparent_logo.png"
    if not os.path.exists(logo_path):
        print(f"Error: {logo_path} not found.")
        return

    img = Image.open(logo_path)
    
    # Get exact bounding box of non-transparent content
    bbox = img.getbbox()
    print(f"Original content bounding box: {bbox}")
    
    cropped = img.crop(bbox)
    width, height = cropped.size
    print(f"Cropped logo size: {width}x{height}")

    # To keep it square, we use the maximum dimension (width) as canvas size
    canvas_size = max(width, height)
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    
    # Center the logo vertically on the square canvas
    offset_x = (canvas_size - width) // 2
    offset_y = (canvas_size - height) // 2
    canvas.paste(cropped, (offset_x, offset_y), cropped)
    print(f"Centered on square canvas at ({offset_x}, {offset_y}) of size {canvas_size}x{canvas_size}")

    # Resampling filter: LANCZOS
    try:
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        resample_filter = Image.ANTIALIAS

    # Generate PNG files
    sizes = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "favicon-48x48.png": 48,
        "favicon-64x64.png": 64,
        "apple-touch-icon.png": 180
    }

    for filename, size in sizes.items():
        resized = canvas.resize((size, size), resample=resample_filter)
        resized.save(filename, "PNG")
        print(f"Saved {filename} ({size}x{size})")

    # Generate multi-resolution ICO file containing 16x16, 32x32, 48x48, 64x64
    ico_img = canvas.copy()
    ico_img.save("favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64)])
    print("Saved favicon.ico (multi-resolution containing 16x16, 32x32, 48x48, 64x64)")

if __name__ == "__main__":
    generate_favicons()
