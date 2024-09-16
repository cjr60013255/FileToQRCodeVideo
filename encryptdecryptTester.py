import os
import re # for creating files and folders sucessfully
from DecodeEncode.FileEncryptor import FileEncryptor # Encrypts Files
from DecodeEncode.FileDecryptor import FileDecryptor  # Decodes binary files to original files
import tkinter as tk # for ease of access in selecting files for processing
from tkinter import filedialog # for ease of access in selecting files for processing

def sanitize_folder_name(name):
    """Remove special characters and spaces from folder names."""
    # Replace spaces with underscores and remove special characters
    sanitized_name = re.sub(r'[<>:"/\\|?*]', '', name)
    sanitized_name = sanitized_name.replace(' ', '_')
    return sanitized_name

def checkBinary(file1Binary, file2Binary):
    if file1Binary == file2Binary:
        return True
    else:
        return False

def main():
    # Default Password and Salt
    password = "HJx5RFHQ5CzrCKdjsdL9cFjjASTwwOWn"
    salt = "1R5eIO1aLNHYRPQorxkAG9Qd75z7IJ1U".encode()

    if len(salt) < 16:
        print("Error: The salt should be at least 16 characters long.")
        return

    action = "e"
    if action == 'e':
        # Create a Tkinter root window and hide it
        root = tk.Tk()
        root.withdraw()

        # Open a file dialog to select the file
        file_path = filedialog.askopenfilename(title="Select a file to encrypt")

        if not file_path:
            print("No file selected. Exiting.")
            return
        
        FileNameWithExtension = os.path.basename(file_path) # "fi le.txt"
        SelectedFileDir = os.path.dirname(file_path) # "C:\Desktop\SomeDir"
        
        # read original file contents as binary data
        with open((file_path), 'rb') as file:
            file1Binary = file.read()

        # Encrypt the file
        print("Encrypt the file")
        encryptor = FileEncryptor(password, salt)
        encryptor.encrypt_file(file_path)

        # RENAME CREATED ENC FILE so that our original file is not overwritten when it is decrypted
        os.rename((file_path + ".enc"), (SelectedFileDir +"/Changed" + FileNameWithExtension + ".enc"))

        print("Decrypt the file")
        decrypter = FileDecryptor(password, salt)
        decrypter.decrypt_file(SelectedFileDir +"/Changed" + FileNameWithExtension + ".enc")

        # read generated file contents as binary data
        with open((SelectedFileDir +"/Changed" + FileNameWithExtension), 'rb') as file:
            file2Binary = file.read()

        #check that the OG file is the same as the generated one
        if checkBinary(file1Binary, file2Binary):
            print("File is the same")
        else:
            print("file is not the same")


main()