def calculateLenOfBinaryData(width = 1920, height = 1080):
    """
    Parameters:
    - image_data: Binary data representing the RGBA pixels.
    - width: The width of the image in pixels. Default resoluton is 1080p
    - height: The height of the image in pixels. Default resoluton is 1080p
    """
    
    color_depth = 32  # Fixed 32-bit (RGBA) color depth
    bytes_per_pixel = color_depth // 8  # 4 bytes per pixel (RGBA)
    row_size = width * bytes_per_pixel  # Row size for 32-bit, no need for padding
    pixel_array_size = row_size * height  # Total size of the pixel array in bytes
    max_pixels = width * height  # Max number of pixels

    # Check if the provided image data size is correct
    print("lenght of data to input = " + str(max_pixels * bytes_per_pixel))

calculateLenOfBinaryData()