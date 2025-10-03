from PIL import Image

# Input PNG file path
input_png = "icon.png"  # Replace with your PNG file
# Output ICO file path
output_ico = "icon.ico"

# Icon sizes for Windows
icon_sizes = [(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)]

# Open the PNG image
img = Image.open(input_png)

# Save as .ico with multiple sizes
img.save(output_ico, format="ICO", sizes=icon_sizes)

print(f"✅ Icon generated: {output_ico}")
