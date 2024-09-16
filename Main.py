import struct
import os
import re # for creating files and folders sucessfully
import getpass # for getting passwords and salts for encryption
from DecodeEncode.FileEncryptor import FileEncryptor # Encrypts Files
from DecodeEncode.FileDecryptor import FileDecryptor  # Decodes binary files to original files
import tkinter as tk # for ease of access in selecting files for processing
from tkinter import filedialog # for ease of access in selecting files for processing
import cv2
import numpy as np

def sanitize_folder_name(name):
    """Remove special characters and spaces from folder names."""
    # Replace spaces with underscores and remove special characters
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '', name)
    sanitized_name = sanitized_name.replace(' ', '_')
    return sanitized_name

def makeDirs(NewFolderDir):
    #create our dirs
    try:
        if not os.path.exists(NewFolderDir):
            os.makedirs(NewFolderDir)
            #print(f"Folder '{NewFolderDir}' created successfully.")
        else:
            print(f"Folder '{NewFolderDir}' already exists.")
        return True
    except OSError as e:
        print(f"An error occurred while creating the folder: {e}")
        return False

def main():
    #paramaters
    imageHeight = 1080
    imageWidth = 1920
    imageColorDepth = 32
    bytes_per_pixel = 4
    binarySplitSize = calculateLenOfBinaryData(imageWidth, imageHeight, imageColorDepth)
    fps = 60  # Frames per second





    # Default Password and Salt
    defaultInputs = True
    if defaultInputs:
        password = "HJx5RFHQ5CzrCKdjsdL9cFjjASTwwOWn"
        salt = "1R5eIO1aLNHYRPQorxkAG9Qd75z7IJ1U".encode()
    else:
        # Input password and salt from the user
        password = getpass.getpass("Enter a password: ")
        salt = getpass.getpass("Enter a salt (at least 16 characters): ").encode()
    
    if len(salt) < 16:
        print("Error: The salt should be at least 16 characters long.")
        return

    # Ask the user whether to encrypt or decrypt
    if defaultInputs:
        action = "e"
    else:
        action = input("Do you want to (E)ncrypt or (D)ecrypt a file? ").strip().lower()

    
    if action not in ['e', 'd']:
        print("Invalid choice. Exiting.")
        return
    if action == 'e':
        # Create a Tkinter root window and hide it
        root = tk.Tk()
        root.withdraw()

        # Open a file dialog to select the file
        file_path = filedialog.askopenfilename(title="Select a file to encrypt")

        if not file_path:
            print("No file selected. Exiting.")
            return

        #figure out folder names and dirs
        FileNameWithExtension = os.path.basename(file_path) # "fi le.txt"
        SelectedFileDir = os.path.dirname(file_path) # "C:\Desktop\SomeDir"
        encrypted_file_path = SelectedFileDir +"/Changed" + FileNameWithExtension + ".enc"
        """FileNameWithourExtension = os.path.splitext(FileNameWithExtension)[0] # "fi le"
        NewFolderName = sanitize_folder_name(FileNameWithourExtension) # "file"
        NewFolderDir = SelectedFileDir + "/" + NewFolderName # "C:\Desktop\SomeDir\file"
        VideoDir = NewFolderDir + "/Video" # "C:\Desktop\SomeDir\file\Video"
        VideoFileDir = VideoDir + "/" + NewFolderName + ".mkv" # "C:\Desktop\SomeDir\file\Video\file.mkv"
        PhotosDir = NewFolderDir + "/Photos" # "C:\Desktop\SomeDir\file\Photos"
        EncryptedFileDir = NewFolderDir +"/" + FileNameWithExtension + ".enc" # "C:\Desktop\SomeDir\file\fi le.enc"
        

        if makeDirs(NewFolderDir) == True:
            makeDirs(VideoDir)
            makeDirs(PhotosDir)
        else:
            print("Could not create folders for some reason\nExiting...\n")
            return"""
        
        # Encrypt the file
        print("Encrypt the file")
        encryptor = FileEncryptor(password, salt)
        encryptor.encrypt_file(file_path)
        
        # RENAME CREATED ENC FILE so that our original file is not overwritten when it is decrypted
        os.rename((file_path + ".enc"), encrypted_file_path)

        # Read encrypted file contents as binary data
        print("Convert encrypted file to binary data")
        with open(encrypted_file_path, 'rb') as file:
            binary_data = file.read()
        
        #split binary data to image sizes
        chunks = split_binary_data(binary_data, binarySplitSize)

            # Create uncompressed AVI
        create_uncompressed_avi_from_binary('output.avi', (imageWidth, imageHeight), chunks, fps)


#--------------------------------------------------PHOTO CREATION AND DECREATION FUNCTIONS--------------------------------------------------


def create_bmp_image_from_binary(save_location, save_file_name, image_data, color_depth = 32, bytes_per_pixel = 4, width = 1920, height = 1080):
    """
    Create a 32-bit BMP image from binary data and save it to a file.

    Parameters:
    - save_location: The directory where the image should be saved.
    - save_file_name: The file name for the saved BMP image.
    - image_data: Binary data representing the RGBA pixel values (4 bytes per pixel).
    - width: The width of the image in pixels.
    - height: The height of the image in pixels.

    Returns:
    - Success message if image is created successfully, or an error if image data is invalid.
    """
    
    #color_depth = 32  # Fixed at 32-bit (RGBA)
    #bytes_per_pixel = 4  # 32-bit means 4 bytes per pixel (R, G, B, A)
    #max_pixels = width * height  # Total number of pixels
    expected_data_size = calculateLenOfBinaryData(width, height, color_depth)

    # Check if the provided image data is too large or too small
    if len(image_data) > expected_data_size:
        print( "Error: Image data exceeds the capacity of the specified dimensions.")
        return
    
    # If the data is smaller, pad the remaining pixels with zeros (transparent pixels)
    if len(image_data) < expected_data_size:
        image_data += b'\x00' * (expected_data_size - len(image_data))  # Pad with zeros (transparent)

    # BMP Header (14 bytes)
    bmp_header = b'BM'
    pixel_array_size = width * height * bytes_per_pixel  # Pixel data size
    file_size = 14 + 40 + pixel_array_size  # 14 for BMP header, 40 for DIB header, rest for pixel data
    reserved = 0
    pixel_array_offset = 14 + 40  # Pixel data starts after BMP + DIB headers
    bmp_header += struct.pack('<I', file_size)  # File size
    bmp_header += struct.pack('<II', reserved, pixel_array_offset)  # Reserved and pixel array offset

    # DIB Header (40 bytes)
    dib_header = struct.pack('<IIIHHIIIIII',
                             40,  # DIB header size
                             width,  # Image width
                             height,  # Image height
                             1,  # Color planes (must be 1)
                             color_depth,  # Bits per pixel (32 bits for RGBA)
                             0,  # Compression (no compression)
                             pixel_array_size,  # Size of the pixel data
                             0,  # Horizontal resolution (not needed)
                             0,  # Vertical resolution (not needed)
                             0,  # Number of colors in the palette (0 for no palette)
                             0)  # Important colors (0 means all are important)

    # Pixel Array (BGRA format, bottom-to-top row order)
    pixel_array = bytearray()
    row_size = width * bytes_per_pixel  # No padding needed for 32-bit BMPs
    for y in range(height - 1, -1, -1):  # BMP stores pixels bottom-to-top
        start = y * row_size
        end = start + row_size
        row_data = image_data[start:end]  # Extract one row of pixel data
        pixel_array += row_data

    # Save the BMP file
    save_path = os.path.join(save_location, save_file_name)
    with open(save_path, 'wb') as f:
        f.write(bmp_header)
        f.write(dib_header)
        f.write(pixel_array)

    return f"Image saved successfully at {save_path}."

def calculateLenOfBinaryData(width = 1920, height = 1080, color_depth = 32):
    """
    Parameters:
    - color depth : depth of color for each pixel
    - width: The width of the image in pixels. Default resoluton is 1080p
    - height: The height of the image in pixels. Default resoluton is 1080p
    """
    color_depth = 32  # Fixed 32-bit (RGBA) color depth
    bytes_per_pixel = color_depth // 8  # 4 bytes per pixel (RGBA)
    max_pixels = width * height  # Max number of pixels
    return max_pixels * bytes_per_pixel

def split_binary_data(data, chunk_size):
    # Ensure the chunk_size is positive
    if chunk_size <= 0:
        raise ValueError("chunk_size must be a positive integer")
    
    # List to store chunks
    chunks = []

    # Iterate over the binary data and split into chunks
    for i in range(0, len(data), chunk_size):
        chunk = data[i:i + chunk_size]
        chunks.append(chunk)
    
    return chunks

#--------------------------------------------------VIDEO CREATION DECREATION FUNCTIONS--------------------------------------------------------
def get_file_locations(dir_path):
    # List to store file paths
    file_locations = []

    # Check if the directory exists
    if not os.path.isdir(dir_path):
        raise ValueError(f"The directory {dir_path} does not exist")

    # Iterate over all files and directories in the given directory
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            # Create the full file path
            file_path = os.path.join(root, file)
            file_locations.append(file_path)
    
    return file_locations

def create_uncompressed_avi(output_file, frame_size, frames, fps=60):
    """
    Create an uncompressed AVI file with 32-bit RGBA pixel depth.

    Parameters:
    - output_file: The name of the output AVI file.
    - frame_size: A tuple (width, height) specifying the size of the video frames.
    - frames: A list of NumPy arrays representing each frame. Each frame should be an array of shape (height, width, 4) for RGBA.
    - fps: Frames per second for the output video.
    """
    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'NONE')  # No compression
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, frame_size, isColor=True)
    
    for frame in frames:
        if frame.shape[2] != 4:
            raise ValueError("Each frame must be an RGBA image with 4 channels.")
        # Convert RGBA to BGRA if needed
        frame_bgra = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGRA)
        video_writer.write(frame_bgra)
    
    video_writer.release()
    print(f"Video saved as {output_file}")

def binary_to_frame(binary_chunk, frame_size):
    """
    Convert a binary chunk into a NumPy array representing an RGBA frame.

    Parameters:
    - binary_chunk: A binary chunk representing one frame.
    - frame_size: A tuple (width, height) specifying the size of the video frame.

    Returns:
    - A NumPy array representing the RGBA frame.
    """
    height, width = frame_size
    bytes_per_pixel = 4  # RGBA
    if len(binary_chunk) != width * height * bytes_per_pixel:
        raise ValueError("Binary chunk size does not match the frame size.")
    
    # Convert binary data to NumPy array and reshape
    frame = np.frombuffer(binary_chunk, dtype=np.uint8).reshape((height, width, bytes_per_pixel))
    return frame

def create_uncompressed_avi_from_binary(output_file, frame_size, chunks, fps=60, bytes_per_pixel = 4):
    """
    Create an uncompressed AVI file from binary data.

    Parameters:
    - output_file: The name of the output AVI file.
    - frame_size: A tuple (width, height) specifying the size of the video frames.
    - binary_data: The complete binary data representing the video.
    - fps: Frames per second for the output video.
    """
    #chunk_size = frame_size[0] * frame_size[1] * bytes_per_pixel
    #chunks = split_binary_data(binary_data, chunk_size)

    # Define the codec and create a VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'NONE')  # No compression
    video_writer = cv2.VideoWriter(output_file, fourcc, fps, frame_size, isColor=True)
    
    for chunk in chunks:
        frame = binary_to_frame(chunk, frame_size)
        # Convert RGBA to BGRA if needed
        frame_bgra = cv2.cvtColor(frame, cv2.COLOR_RGBA2BGRA)
        video_writer.write(frame_bgra)
    
    video_writer.release()
    print(f"Video saved as {output_file}")

"""# Example usage
width, height = 1920, 1080  # Video dimensions
fps = 24  # Frames per second

# Example binary data: create some dummy data for testing
# Create a video with 10 frames of solid red
frame_data = np.full((height, width, 4), (255, 0, 0, 255), dtype=np.uint8)
binary_data = frame_data.tobytes() * 10  # 10 frames

# Create uncompressed AVI
create_uncompressed_avi_from_binary('output.avi', (width, height), binary_data, fps)"""


main()