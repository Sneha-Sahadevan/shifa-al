from PIL import Image

# Open the image
img = Image.open(r"C:\Users\SNEHA SAHADEVAN\.gemini\antigravity\brain\b18d8b89-81c7-4c7a-9489-5f39297ff9fb\media__1776708474094.png")
width, height = img.size
print(f"Original size: {width}x{height}")

# Crop parameters - estimate: top text is roughly top 30%, bottom logos are bottom 15%
top = int(height * 0.3)
bottom = int(height * 0.85)

cropped = img.crop((0, top, width, bottom))
cropped.save("assets/beard_laser.jpg", quality=90)
print("Cropped successfully array size: ", cropped.size)
