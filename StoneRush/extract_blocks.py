"""
Extract block sprites from screenshots
"""
from PIL import Image
import os

def remove_cyan_background(img):
    """Remove cyan/light blue background and make transparent"""
    img = img.convert("RGBA")
    data = img.getdata()
    new_data = []

    for item in data:
        r, g, b, a = item
        # Check if pixel is already transparent
        if a == 0:
            new_data.append((0, 0, 0, 0))
        # Check if pixel is cyan/light blue (RGB around 152, 216, 235)
        elif (r >= 140 and r <= 165 and g >= 200 and g <= 230 and b >= 225 and b <= 245):
            # Make transparent
            new_data.append((0, 0, 0, 0))
        else:
            # Keep pixel - this is part of the block (gray, black, etc)
            new_data.append(item)

    img.putdata(new_data)
    return img

# Load screenshots
assets_dir = "assets"
import_dir = "import"

# Screenshot 1 - Ground block with stairs (540x552)
img1 = Image.open(os.path.join(import_dir, "Screenshot 2025-12-30 143005.png"))
print(f"Screenshot 1 size: {img1.size}")

# Screenshot 2 - Cracked block (732x720)
img2 = Image.open(os.path.join(import_dir, "Screenshot 2025-12-30 143430.png"))
print(f"Screenshot 2 size: {img2.size}")

# The screenshots show single block sprites with cyan background
# We need to crop to just the block (remove empty space) and resize to 32x32

# Process screenshot 1 (ground block)
img1_rgba = img1.convert("RGBA")
# Remove cyan background FIRST
img1_clean = remove_cyan_background(img1_rgba)

# Now find bounding box of non-transparent pixels
bbox1 = img1_clean.getbbox()
if bbox1:
    print(f"Ground block bounding box: {bbox1}")
    # Crop to the block
    block1 = img1_clean.crop(bbox1)
    print(f"Ground block cropped size: {block1.size}")
    # Resize to 32x32 (keep aspect ratio by using the larger dimension)
    block1 = block1.resize((32, 32), Image.Resampling.LANCZOS)
    # Save
    block1.save(os.path.join(assets_dir, "block_ground.png"))
    print(f"Saved block_ground.png (32x32)")

# Process screenshot 2 (cracked block)
img2_rgba = img2.convert("RGBA")
# Remove cyan background FIRST
img2_clean = remove_cyan_background(img2_rgba)

# Find bounding box
bbox2 = img2_clean.getbbox()
if bbox2:
    print(f"Cracked block bounding box: {bbox2}")
    # Crop to the block
    block2 = img2_clean.crop(bbox2)
    print(f"Cracked block cropped size: {block2.size}")
    # Resize to 32x32
    block2 = block2.resize((32, 32), Image.Resampling.LANCZOS)
    # Save
    block2.save(os.path.join(assets_dir, "block_cracked.png"))
    print(f"Saved block_cracked.png (32x32)")

print("Done!")
