def extract_message(image_path):
    img = Image.open(image_path)
    pixels = list(img.getdata())

    binary_message = ""
    for pixel in pixels:
        for i in range(3):
            binary_message += str(pixel[i] & 1)

    # Convert binary to text
    message = ""
    for i in range(0, len(binary_message), 8):
        char = chr(int(binary_message[i:i+8], 2))
        if char == '\xFE':  # Stop delimiter
            break
        message += char

    return message

# Usage
hidden_msg = extract_message("output.png")
print("Hidden Message:", hidden_msg)