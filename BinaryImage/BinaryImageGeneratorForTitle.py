import os
from PIL import Image

class BinaryImageGeneratorForTitle:
    def __init__(self, text, output_dir, image_size=(1920, 1080)):
        self.text = text
        self.output_dir = output_dir
        self.image_size = image_size
        self.pixels_per_image = image_size[0] * self.image_size[1]
        
        # Check if text length exceeds the limit
        if len(text) > 255:
            raise ValueError("Text exceeds the maximum allowed length of 255 characters.")
    
    def text_to_binary(self):
        # Convert text to binary string
        return ''.join(f'{ord(char):08b}' for char in self.text)
    
    def generate_image_from_text(self):
        binary_data = self.text_to_binary()
        
        # Ensure the binary data fits into the image
        if len(binary_data) > self.pixels_per_image:
            raise ValueError("Text is too long to fit in the image. Reduce text length.")
        
        # Pad the binary data to fill the image
        binary_data = binary_data.ljust(self.pixels_per_image, '0')

        # Create a new binary image
        img = Image.new('1', self.image_size)  # Mode '1' means 1-bit pixels (black and white)
        pixels = img.load()

        # Fill the image with binary data
        for i in range(self.pixels_per_image):
            x = i % self.image_size[0]
            y = i // self.image_size[0]
            pixels[x, y] = int(binary_data[i])  # Set the pixel to black (1) or white (0)

        # Save the image
        output_file = os.path.join(self.output_dir, "encrypted_image_0.png")
        img.save(output_file)
        #print(f"Image saved as {output_file}")

'''# Example usage
if __name__ == "__main__":
    text = "Sample text to encode"  # Replace with actual text
    output_dir = 'path/to/output'
    encoder = BinaryImageGeneratorForTitle(text, output_dir)
    encoder.generate_image_from_text()
'''
