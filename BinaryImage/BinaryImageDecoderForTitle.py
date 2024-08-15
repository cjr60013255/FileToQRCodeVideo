import os
from PIL import Image

class BinaryImageDecoderForTitle:
    def __init__(self, image_file, image_size=(1920, 1080)):
        self.image_file = image_file
        self.image_size = image_size
        self.pixels_per_image = image_size[0] * image_size[1]
        self.text = ""
        
        # Check if the image file exists
        if not os.path.isfile(self.image_file):
            raise FileNotFoundError(f"The file {self.image_file} does not exist.")
    
    def extract_binary_from_image(self):
        # Open the image
        img = Image.open(self.image_file)
        img = img.convert('1')  # Convert to black and white (1-bit pixels)
        pixels = img.load()
        
        # Extract binary data from the image
        binary_data = ''
        for y in range(self.image_size[1]):
            for x in range(self.image_size[0]):
                binary_data += '1' if pixels[x, y] == 255 else '0'  # 255 for white, 0 for black
        
        # Return binary data trimmed to the original length
        return binary_data[:self.pixels_per_image]
    
    def binary_to_text(self, binary_data):
        # Split the binary data into 8-bit chunks and convert to text
        text = ''.join(chr(int(binary_data[i:i + 8], 2)) for i in range(0, len(binary_data), 8))
        # Remove padding null characters
        cleaned_text = text.rstrip('\x00')
        # Exclude any all-zero data
        if not cleaned_text.strip('\x00'):
            print("No valid text found in the image.")
            return ""
        return cleaned_text
    
    def decode_text_from_image(self):
        binary_data = self.extract_binary_from_image()
        self.text = self.binary_to_text(binary_data)

'''# Example usage
if __name__ == "__main__":
    image_file = 'path/to/encrypted_image_0.png'  # Replace with the path to the image
    decoder = BinaryImageDecoderForTitle(image_file)
    decoder.decode_text_from_image()
'''