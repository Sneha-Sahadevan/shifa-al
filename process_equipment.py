import os
import io
import traceback
from PIL import Image
from rembg import remove

assets_dir = r"c:\Users\SNEHA SAHADEVAN\OneDrive\Desktop\shifa al\assets"
files = ['gentle.jpeg', 'spectra.jpeg', 'eco2.jpeg', 'hydrafacial.jpeg', 'scalp.jpeg']

for f in files:
    print(f"Processing {f}...")
    in_path = os.path.join(assets_dir, f)
    out_path = os.path.join(assets_dir, f.replace('.jpeg', '.png').replace('.jpg', '.png'))
    try:
        with open(in_path, 'rb') as i:
            input_data = i.read()
            
        output_data = remove(input_data)
        
        # Load the output image
        img = Image.open(io.BytesIO(output_data))
        
        # Create a white background image
        new_img = Image.new('RGB', img.size, (255, 255, 255))
        
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # Paste the image on the background using the alpha channel as mask
            new_img.paste(img, (0, 0), img.convert('RGBA'))
        else:
            new_img.paste(img, (0, 0))
            
        new_img.save(out_path, format="PNG")
        print(f"Saved {out_path}")
    except Exception as e:
        print(f"Error on {f}: {e}")
        traceback.print_exc()
