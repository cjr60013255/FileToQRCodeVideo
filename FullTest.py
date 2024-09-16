import os
import tempfile
import subprocess
import numpy as np
import tkinter as tk # for ease of access in selecting files for processing
from tkinter import filedialog # for ease of access in selecting files for processing
from DecodeEncode.FileEncryptor import FileEncryptor # Encrypts Files
from DecodeEncode.FileDecryptor import FileDecryptor  # Decodes binary files to original files

##----------------------------------------supporting Functions------------------------------------
#takes two binary entries and compares them
def checkBinary(file1Binary, file2Binary):
    if file1Binary == file2Binary:
        return True
    else:
        return False
    
#calculates chunk data stuff
def calculateLenOfBinaryData(width, height):
    """
    Calculates the size of binary data needed for yuv420p format.
    """
    Y_size = width * height
    U_size = (width // 2) * (height // 2)
    V_size = (width // 2) * (height // 2)
    return Y_size + U_size + V_size

#splits binary data into specified lengths
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

#takes generated binary data blocks into frames
def binary_to_frame(binary_chunks, width, height):
    frames = []
    Y_size = width * height
    U_size = (width // 2) * (height // 2)
    V_size = (width // 2) * (height // 2)

    for i, binary_chunk in enumerate(binary_chunks):
        if i == len(binary_chunks) - 1 and len(binary_chunk) < (Y_size + U_size + V_size):
            padding_size = (Y_size + U_size + V_size) - len(binary_chunk)
            binary_chunk = binary_chunk + (b'\x00' * padding_size)

        Y = binary_chunk[:Y_size]
        U = binary_chunk[Y_size:Y_size + U_size]
        V = binary_chunk[Y_size + U_size:Y_size + U_size + V_size]

        frame = np.zeros((height + height // 2, width), dtype=np.uint8)
        frame[:height, :width] = np.frombuffer(Y, dtype=np.uint8).reshape((height, width))
        frame[height:, :width // 2] = np.frombuffer(U, dtype=np.uint8).reshape((height // 2, width // 2))
        frame[height:, width // 2:] = np.frombuffer(V, dtype=np.uint8).reshape((height // 2, width // 2))
        
        frames.append(frame)

    return frames

#----------------------------------------main Functions------------------------------------
#Encrypts a file and Decrypts a file
def encrypt_decrypt(file_path, FileNameWithExtension, SelectedFileDir, encrypted_file_path, decrypted_file_path):

    # Default Password and Salt
    password = "HJx5RFHQ5CzrCKdjsdL9cFjjASTwwOWn"
    salt = "1R5eIO1aLNHYRPQorxkAG9Qd75z7IJ1U".encode()

    if len(salt) < 16:
        print("Error: The salt should be at least 16 characters long.")
        return
        
    # read original file contents as binary data
    with open((file_path), 'rb') as file:
        file1Binary = file.read()

    # Encrypt the file
    print("Encrypt the file")
    encryptor = FileEncryptor(password, salt)
    encryptor.encrypt_file(file_path)

    # RENAME CREATED ENC FILE so that our original file is not overwritten when it is decrypted
    os.replace((file_path + ".enc"), encrypted_file_path)

    print("Decrypt the file")
    decrypter = FileDecryptor(password, salt)
    decrypter.decrypt_file(encrypted_file_path)

    # read generated file contents as binary data
    with open(decrypted_file_path, 'rb') as file:
        file2Binary = file.read()

    #check that the OG file is the same as the generated one
    if checkBinary(file1Binary, file2Binary):
        print("DECRYPTING AND ENCRYPTING WAS SUCCESSFUL.")
        return True
    else:
        print("DECRYPTING AND ENCRYPTING FAILED!")
        return False

#Makes video from Encrypted File
def makeVideo(encrypted_file_path, SelectedFileDir, binarySplitSize, VideoFileName, ffmpeg_path, imageHeight, imageWidth, fps):
    with open(encrypted_file_path, 'rb') as file:
        file1Binary = file.read()

    file_1_chunks = split_binary_data(file1Binary, binarySplitSize)
    file_1_frames = binary_to_frame(file_1_chunks, imageWidth, imageHeight)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.raw') as temp_file:
        raw_video_path = temp_file.name
        
        with open(raw_video_path, 'wb') as f:
            for frame in file_1_frames:
                f.write(frame.tobytes())

    # Create MP4 video using FFmpeg with H.264 codec
    ffmpeg_command = [
        ffmpeg_path,
        '-f', 'rawvideo',
        '-pix_fmt', 'yuv420p',
        #'-hide_banner',  # Hide version and startup information
        '-s', f'{imageWidth}x{imageHeight}',
        '-r', str(fps),
        '-i', raw_video_path,
        '-c:v', 'libx264',
        VideoFileName
    ]
    
    try:
        subprocess.run(ffmpeg_command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except FileNotFoundError:
        print(f"Error: {ffmpeg_path} not found. Make sure ffmpeg is installed and the path is correct.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while creating the video: {e}")
        return False
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return False

    os.remove(raw_video_path)
    os.replace(VideoFileName, os.path.join(SelectedFileDir, VideoFileName))

    return True
    
#----------------------------------------MAIN Function------------------------------------
def main():
    #get Our test File
    # Create a Tkinter root window and hide it
    root = tk.Tk()
    root.withdraw()
    # Open a file dialog to select the file
    file_path = filedialog.askopenfilename(title="Select a file to encrypt")
    if not file_path:
        print("No file selected. Exiting.")
        return

    #File paths
    FileNameWithExtension = os.path.basename(file_path) # "fi le.txt"
    SelectedFileDir = os.path.dirname(file_path) # "C:\Desktop\SomeDir"
    encrypted_file_path = SelectedFileDir +"/" + "Enc_" + FileNameWithExtension + ".enc"
    decrypted_file_path = SelectedFileDir +"/" + "Enc_" + FileNameWithExtension
    VideoFileName = FileNameWithExtension + ".mp4"

    #Video paramaters
    imageHeight = 1080
    imageWidth = 1920
    imageColorDepth = 8
    bytes_per_pixel = 1.5
    binarySplitSize = calculateLenOfBinaryData(imageWidth, imageHeight)
    fps = 30
    ffmpeg_path = 'ffmpeg'
    
    #Starting Tests
    if encrypt_decrypt(file_path, FileNameWithExtension, SelectedFileDir, encrypted_file_path, decrypted_file_path):
        if makeVideo(encrypted_file_path, SelectedFileDir, binarySplitSize, VideoFileName, ffmpeg_path, imageHeight, imageWidth, fps):
            return True
        else:
            return False
    else:
        return False    

#start everything
passed = main()
if passed:
    print("All Tests Passed")
else:
    print("Failed Tests")