import os
import glob
from PIL import Image
import sys

assets_dir = 'assets'
files = glob.glob(os.path.join(assets_dir, 'frame_*.png'))

print(f"Found {len(files)} files to compress.")

for idx, file in enumerate(files):
    try:
        img = Image.open(file)
        # Convert to RGB to safely save as WebP (removes alpha if any, but usually these are video frames)
        if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
            # If transparency is truly needed, we can keep RGBA, but WebP handles RGBA.
            pass
        
        if img.width > 1280:
            ratio = 1280 / img.width
            new_h = int(img.height * ratio)
            img = img.resize((1280, new_h), Image.Resampling.LANCZOS)
        
        webp_file = file.replace('.png', '.webp')
        img.save(webp_file, 'WEBP', quality=50)
        
        # Remove original PNG to save space
        os.remove(file)
        
        if idx % 10 == 0:
            print(f"Processed {idx+1}/{len(files)}...")
            
    except Exception as e:
        print(f"Error processing {file}: {e}")

print("Compression complete!")
