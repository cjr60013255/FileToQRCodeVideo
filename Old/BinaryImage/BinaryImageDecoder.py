import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

class BinaryImageDecoder:
    def __init__(self, input_dir, output_file, image_size=(1920, 1080), num_threads=8):
        self.input_dir = input_dir
        self.output_file = output_file
        self.image_size = image_size
        self.pixels_per_image = image_size[0] * image_size[1]
        self.num_threads = num_threads  # Number of threads to use
        self.binary_data = ""

    def _extract_binary_from_image(self, image_file):
        """Extract binary data from a single image."""
        img = Image.open(image_file)
        img = img.convert('1')  # Convert to black and white (1-bit pixels)
        pixels = img.load()
        
        binary_data = ""
        for y in range(self.image_size[1]):
            for x in range(self.image_size[0]):
                binary_data += '1' if pixels[x, y] == 255 else '0'  # 255 for white, 0 for black

        return binary_data

    def decode_images_to_binary(self):
        """Decode all images from the input directory, skipping encrypted_image_0.png."""
        # Gather all relevant image files, sorted by number
        image_files = sorted(
            [f for f in os.listdir(self.input_dir) if f.startswith("encrypted_image_") and f.endswith(".png")],
            key=lambda x: int(x.split('_')[-1].split('.')[0])
        )

        # Skip encrypted_image_0.png
        image_files = [f for f in image_files if f != "encrypted_image_0.png"]

        # Use a ThreadPoolExecutor to process images in parallel
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            results = executor.map(
                self._extract_binary_from_image,
                [os.path.join(self.input_dir, f) for f in image_files]
            )

        # Combine the binary data from all images
        self.binary_data = ''.join(results)
        #print("Binary data extracted from images.")

    def binary_to_original_data(self):
        """Convert binary data back to its original format."""
        # Convert binary string back to bytes
        data = bytearray(int(self.binary_data[i:i + 8], 2) for i in range(0, len(self.binary_data), 8))
        return data

    def save_to_file(self):
        """Save the decoded data to a .enc file."""
        original_data = self.binary_to_original_data()
        with open(self.output_file, 'wb') as file:
            file.write(original_data)
        #print(f"Data saved to {self.output_file}")

    def decode(self):
        """Full decoding process."""
        self.decode_images_to_binary()
        self.save_to_file()

'''# Example usage
if __name__ == "__main__":
    input_dir = 'path/to/output'  # Replace with the directory where the images are stored
    output_file = 'path/to/output/decoded_data.enc'  # Replace with the desired output file path
    decoder = BinaryImageDecoder(input_dir, output_file, num_threads=8)  # Adjust num_threads as needed
    decoder.decode()
'''