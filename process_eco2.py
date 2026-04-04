from PIL import Image
import os

assets_dir = r"c:\Users\SNEHA SAHADEVAN\OneDrive\Desktop\shifa al\assets"
img_path = os.path.join(assets_dir, 'eco2.jpeg')
out_path = os.path.join(assets_dir, 'eco2.jpeg') # Overwrite or save as eco2_white.jpg

img = Image.open(img_path).convert("RGBA")
pixels = img.load()

width, height = img.size

# Sample the background color from the top-left corner
bg_color = pixels[0, 0][:3]

# A simple threshold to make near-background pixels white
# We will check if the pixel is close to bg_color
tolerance = 20

for y in range(height):
    for x in range(width):
        r, g, b, a = pixels[x, y]
        # Calculate distance from background
        if (abs(r - bg_color[0]) < tolerance and 
            abs(g - bg_color[1]) < tolerance and 
            abs(b - bg_color[2]) < tolerance):
            # Make it pure white
            pixels[x, y] = (255, 255, 255, 255)
        elif r > 230 and g > 230 and b > 230:
             # Also make very light pixels white to remove any gradient
             pixels[x, y] = (255, 255, 255, 255)

# Save as new file just to be safe
out_path = os.path.join(assets_dir, 'eco2_white.jpg')
img.convert("RGB").save(out_path, "JPEG")
print(f"Saved {out_path}")
