import os
from PIL import Image

def generate_favicons():
    logo_path = "assets/transparent_logo.png"
    if not os.path.exists(logo_path):
        print(f"Error: {logo_path} not found.")
        return

    img = Image.open(logo_path)
    
    # Crop the icon (Segment 1 bounds detected: X: 19 to 278, Y: 36 to 346)
    x1, y1, x2, y2 = 19, 36, 278, 346
    icon = img.crop((x1, y1, x2 + 1, y2 + 1))
    print(f"Isolated icon size: {icon.size}")
    
    # We want to place the icon on a square canvas with a nice, professional padding
    # Icon size is 260x311. Let's use a 360x360 canvas.
    canvas_size = 360
    canvas = Image.new("RGBA", (canvas_size, canvas_size), (0, 0, 0, 0))
    
    # Calculate offset to center the icon
    offset_x = (canvas_size - icon.width) // 2
    offset_y = (canvas_size - icon.height) // 2
    canvas.paste(icon, (offset_x, offset_y), icon)
    print(f"Pasted icon at ({offset_x}, {offset_y}) on a {canvas_size}x{canvas_size} canvas.")

    # Resampling filter: LANCZOS (fallback to ANTIALIAS for older Pillow versions)
    try:
        resample_filter = Image.Resampling.LANCZOS
    except AttributeError:
        resample_filter = Image.ANTIALIAS

    # Generate PNG files
    sizes = {
        "favicon-16x16.png": 16,
        "favicon-32x32.png": 32,
        "favicon-48x48.png": 48,
        "apple-touch-icon.png": 180
    }

    for filename, size in sizes.items():
        resized = canvas.resize((size, size), resample=resample_filter)
        resized.save(filename, "PNG")
        print(f"Saved {filename} ({size}x{size})")

    # Generate multi-resolution ICO file containing 16x16, 32x32, and 48x48
    # ICO expects sizes as a list of tuples
    ico_img = canvas.copy()
    ico_img.save("favicon.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48)])
    print("Saved favicon.ico (multi-resolution containing 16x16, 32x32, 48x48)")

if __name__ == "__main__":
    generate_favicons()
