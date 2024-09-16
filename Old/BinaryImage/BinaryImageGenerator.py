import os
from PIL import Image
from concurrent.futures import ThreadPoolExecutor

class BinaryImageGenerator:
    def __init__(self, binary_data, output_dir, image_size=(1920, 1080), num_threads=8):
        self.binary_data = binary_data
        self.output_dir = output_dir
        self.image_size = image_size
        self.pixels_per_image = image_size[0] * image_size[1]
        self.num_threads = num_threads  # Number of threads to use

    def binary_string_from_data(self):
        return ''.join(f'{byte:08b}' for byte in self.binary_data)

    def _generate_image_chunk(self, chunk, image_number):
        """Generate an image from a binary chunk."""
        img = Image.new('1', self.image_size)  # Create a new binary image (mode '1' means 1-bit pixels)
        pixels = img.load()

        for j in range(len(chunk)):
            x = j % self.image_size[0]
            y = j // self.image_size[0]
            pixels[x, y] = int(chunk[j])  # Set the pixel to black (1) or white (0)

        img.save(os.path.join(self.output_dir, f"encrypted_image_{image_number}.png"))

    def generate_images_from_binary(self):
        binary_data = self.binary_string_from_data()
        image_number = 1
        chunks = []

        for i in range(0, len(binary_data), self.pixels_per_image):
            chunk = binary_data[i:i + self.pixels_per_image]
            chunk += '0' * (self.pixels_per_image - len(chunk))  # Pad the last chunk with zeros if needed
            chunks.append((chunk, image_number))
            image_number += 1

        # Use a ThreadPoolExecutor to process images in parallel
        with ThreadPoolExecutor(max_workers=self.num_threads) as executor:
            for chunk, number in chunks:
                executor.submit(self._generate_image_chunk, chunk, number)

        #print(f"{len(chunks)} images generated and saved in {self.output_dir}")

'''# Example usage
if __name__ == "__main__":
    binary_data = bytearray()  # Replace with actual binary data
    output_dir = 'path/to/output'
    generator = BinaryImageGenerator(binary_data, output_dir, num_threads=8)  # Adjust num_threads as needed
    generator.generate_images_from_binary()
'''