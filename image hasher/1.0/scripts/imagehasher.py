from PIL import Image
import hashlib

def pixel_to_sha(pixel):
    r, g, b = pixel
    pixel_string = f"{r},{g},{b}"
    return hashlib.sha256(pixel_string.encode()).hexdigest()

def hash_image(input_path, output_path):
    img = Image.open(input_path).convert("RGB")
    width, height = img.size

    with open(output_path, "w") as f:
        f.write(f"{width}x{height}\n")

        for y in range(height):
            row_data = []
            for x in range(width):
                pixel = img.getpixel((x,y))
                sha_hex = pixel_to_sha(pixel)
                row_data.append(f"{sha_hex}:{pixel[0]},{pixel[1]},{pixel[2]}")
                f.write("|".join(row_data)+"\n")

inputpath = input('input the path to the image: ')
outputpath = input('input the path to the output of the image (save as txt): ')

hash_image(inputpath, outputpath)

# Example usage:

# input the path to the image:
# "input.png"

# input the path to the output of the image (save as txt):
# "output.txt"