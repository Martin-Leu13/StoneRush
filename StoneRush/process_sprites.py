"""
Utility script to remove blue background from sprites and make them transparent
"""
from PIL import Image
import os


def remove_blue_background(input_path, output_path):
    """Remove blue/cyan background and make it transparent"""
    # Open image
    img = Image.open(input_path)
    img = img.convert("RGBA")

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

    # Process player sprites
    remove_blue_background(
        os.path.join(assets_dir, "player_idle.png"),
        os.path.join(assets_dir, "player_idle.png")
    )

    remove_blue_background(
        os.path.join(assets_dir, "player_walk.png"),
        os.path.join(assets_dir, "player_walk.png")
    )

    print("Done! Blue backgrounds removed.")
