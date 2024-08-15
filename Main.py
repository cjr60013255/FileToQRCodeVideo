import getpass # for getting passwords and salts for encryption
import os # for creating files and folders
import re # for creating files and folders sucessfully
import tkinter as tk # for ease of access in selecting files for processing
from tkinter import filedialog # for ease of access in selecting files for processing
from DecodeEncode.FileEncryptor import FileEncryptor # Encrypts Files
from BinaryImage.BinaryImageGenerator import BinaryImageGenerator # Converts files to QR codes
from PhotoVideo.PhotoToVideoConverter import PhotoToVideoConverter # Converts QR Code images to Video
from BinaryImage.BinaryImageGeneratorForTitle import BinaryImageGeneratorForTitle # Converts file name to QR Code image
from BinaryImage.BinaryImageDecoder import BinaryImageDecoder # converts QR Code images to Binary file
from DecodeEncode.FileDecryptor import FileDecryptor  # Decodes binary files to original files
from PhotoVideo.VideoToImageExtractor import VideoToImageExtractor  # converts videos to QR Code images
from BinaryImage.BinaryImageDecoderForTitle import BinaryImageDecoderForTitle # gets the original Title from QR Codes

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
    # Default Password and Salt
    defaultInputs = True
    if defaultInputs:
        password = "HJx5RFHQ5CzrCKdjsdL9cFjjASTwwOWn"
        salt = "1R5eIO1aLNHYRPQorxkAG9Qd75z7IJ1U".encode()
    else:
        # Input password and salt from the user
        password = getpass.getpass("Enter a password: ")
        salt = getpass.getpass("Enter a salt (at least 16 characters recommended): ").encode()
    
    if len(salt) < 16:
        print("Error: The salt should be at least 16 characters long.")
        return

    # Ask the user whether to encrypt or decrypt
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
        FileNameWithourExtension = os.path.splitext(FileNameWithExtension)[0] # "fi le"
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
            return
        
        # Encrypt the file
        print("Encrypt the file")
        encryptor = FileEncryptor(password, salt)
        encryptor.encrypt_file(file_path)
        
        # Move the encrypted file to the newly created folder
        os.rename((file_path + ".enc"), EncryptedFileDir)
        #print("\n\n\n" + file_path + ".enc - to - \"" + EncryptedFileDir + "\"\n\n\n")

        
        
        # Convert encrypted file contents to binary data
        print("Convert encrypted file to binary data")
        with open(EncryptedFileDir, 'rb') as file:
            binary_data = file.read()
        
        # Generate image from file name
        encoder = BinaryImageGeneratorForTitle(FileNameWithExtension, PhotosDir)
        encoder.generate_image_from_text()

        # Generate images from binary data
        print("Generate images from binary data")
        binary_image_generator = BinaryImageGenerator(binary_data, PhotosDir)
        binary_image_generator.generate_images_from_binary()
        
        # Convert images to video
        image_to_video_converter = PhotoToVideoConverter(PhotosDir, VideoFileDir)
        image_to_video_converter.convert()
        
        print(f"Video '{VideoFileDir}' created successfully.")
        print("Finished!")

    elif action == 'd':

        # Create a Tkinter root window and hide it
        root = tk.Tk()
        root.withdraw()

        # Open a file dialog to select the file
        file_path = filedialog.askopenfilename(title="Select a file to decrypt")

        if not file_path:
            print("No file selected. Exiting.")
            return

        #figure out folder names and dirs
        FileNameWithExtension = os.path.basename(file_path) # "video.mkv"
        SelectedFileDir = os.path.dirname(file_path) # "C:\Desktop\SomeDir"
        FileNameWithourExtension = os.path.splitext(FileNameWithExtension)[0] # "fi le"
        NewFolderName = sanitize_folder_name(FileNameWithourExtension) # "file"
        NewFolderDir = SelectedFileDir + "/" + NewFolderName # "C:\Desktop\SomeDir\file"
        OutputDir = NewFolderDir + "/Output" # "C:\Desktop\SomeDir\file\Output"
        PhotosDir = NewFolderDir + "/Photos" # "C:\Desktop\SomeDir\file\Photos"
        

        if makeDirs(NewFolderDir) == True:
            makeDirs(OutputDir)
            makeDirs(PhotosDir)
        else:
            print("Could not create folders for some reason\nExiting...\n")
            return
    
        # Extract photos from video
        print("Extract photos from video")
        extractor = VideoToImageExtractor((SelectedFileDir + "/" + FileNameWithExtension), (PhotosDir+"/"))
        extractor.extract()

        # Get Title of encrypted File
        print("Get Title of encrypted File")
        decoder = BinaryImageDecoderForTitle((PhotosDir + "\\encrypted_image_0.png"))
        decoder.decode_text_from_image()
        EncryptedFileDir = NewFolderDir +"/" + decoder.text +".enc" # "C:\Desktop\SomeDir\file\fi le.enc"

        # Restore encrypted binary file
        print("Restore encrypted binary file")
        decoder2 = BinaryImageDecoder(PhotosDir, EncryptedFileDir)  # Adjust num_threads as needed
        decoder2.decode()

        # Decrypt file to original
        print("Decrypt the file")
        decryptor = FileDecryptor(password, salt)
        decryptor.decrypt_file(EncryptedFileDir)

if __name__ == "__main__":
    main()
