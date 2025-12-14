from PIL import Image

def unhash_image(input_path, output_path):
    try:
        with open(input_path, "r") as f:
            size_line = f.readline().strip()
            width, height = map(int, size_line.split("x"))

        img = Image.new("RGB", (width, height))

        with open(input_path, "r") as f:
            f.readline()
            y = 0
            line_count = 0
            
            for line in f:
                if not line.strip():
                    continue
                
                pixel_entries = line.strip().split("|")
                for x, entry in enumerate(pixel_entries):
                    if x >= width:
                        break
                    if entry.strip():
                        try:
                            _, rgb_part = entry.split(":")
                            r, g, b = map(int, rgb_part.split(","))
                            img.putpixel((x, y), (r, g, b))
                        except ValueError:
                            continue
                
                line_count += 1
                if line_count % width == 0:
                    y += 1
                    if y >= height:
                        break
        
        img.save(output_path)
        print(f"Reconstructed image saved as {output_path}")
    except FileNotFoundError:
        print(f"Error: File '{input_path}' not found.")
    except ValueError as e:
        print(f"Error: Invalid data format - {e}")
    except Exception as e:
        print(f"An error occurred: {e}")

inputpath = input('input the path to the image (the text file with the hash): ')
outputpath = input('input the path to the output of the image (save as image): ')

unhash_image(inputpath, outputpath)

# Example usage:

# input the path to the image (the text file with the hash):
# "output.txt"

# input the path to the output of the image (save as image):
# "restored.png"

