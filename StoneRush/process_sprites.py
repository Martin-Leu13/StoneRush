"""
Utility script to remove blue background from sprites and make them transparent
"""
from PIL import Image
import os


def remove_blue_background(input_path, output_path, target_size=None):
    """Remove blue/cyan background and make it transparent

    Args:
        input_path: Path to input image
        output_path: Path to save output image
        target_size: Optional (width, height) tuple to resize to before processing
    """
    # Open image
    img = Image.open(input_path)
    img = img.convert("RGBA")

    # Resize to target size if specified
    if target_size:
        img = img.resize(target_size, Image.Resampling.LANCZOS)

    # Get pixel data
    data = img.getdata()
    new_data = []

    # The background color appears to be light cyan RGB around (135, 206, 235)
    # We'll use a threshold to catch similar colors
    for item in data:
        r, g, b, a = item

        # Check if pixel is cyan/light blue (sky color)
        # Cyan has: high blue, medium-high green, lower red
        # Allow some tolerance for similar shades
        if (r < 200 and g > 170 and b > 200):  # Cyan range
            # Make it transparent
            new_data.append((0, 0, 0, 0))
        else:
            # Keep the pixel
            new_data.append(item)

    # Update image data
    img.putdata(new_data)

    # Save
    img.save(output_path)
    print(f"Processed: {output_path}")


if __name__ == "__main__":
    assets_dir = os.path.join(os.path.dirname(__file__), "assets")

    # Standard size for all player sprites (square for easier scaling)
    SPRITE_SIZE = (32, 32)

    print("Processing sprites...")
    print(f"Target size: {SPRITE_SIZE}")

    # Process player sprites - resize to same size first!
    remove_blue_background(
        os.path.join(assets_dir, "player_idle.png"),
        os.path.join(assets_dir, "player_idle.png"),
        target_size=SPRITE_SIZE
    )

    remove_blue_background(
        os.path.join(assets_dir, "player_walk.png"),
        os.path.join(assets_dir, "player_walk.png"),
        target_size=SPRITE_SIZE
    )

    # Verify both sprites are the same size
    idle_img = Image.open(os.path.join(assets_dir, "player_idle.png"))
    walk_img = Image.open(os.path.join(assets_dir, "player_walk.png"))
    print(f"\nVerification:")
    print(f"  player_idle.png: {idle_img.size}")
    print(f"  player_walk.png: {walk_img.size}")
    if idle_img.size == walk_img.size:
        print(f"[OK] Both sprites are now the same size!")
    else:
        print(f"[WARNING] Sprites still have different sizes!")

    # Process block sprites
    print(f"\nProcessing block sprites...")
    remove_blue_background(
        os.path.join(assets_dir, "block_ground.png"),
        os.path.join(assets_dir, "block_ground.png"),
        target_size=SPRITE_SIZE
    )

    remove_blue_background(
        os.path.join(assets_dir, "block_cracked.png"),
        os.path.join(assets_dir, "block_cracked.png"),
        target_size=SPRITE_SIZE
    )

    # Verify block sprites
    ground_img = Image.open(os.path.join(assets_dir, "block_ground.png"))
    cracked_img = Image.open(os.path.join(assets_dir, "block_cracked.png"))
    print(f"\nBlock sprite verification:")
    print(f"  block_ground.png: {ground_img.size}")
    print(f"  block_cracked.png: {cracked_img.size}")
    if ground_img.size == cracked_img.size == SPRITE_SIZE:
        print(f"[OK] Both block sprites are the correct size!")
    else:
        print(f"[WARNING] Block sprite sizes don't match!")

    print("\nDone! Blue backgrounds removed and sprites resized.")
