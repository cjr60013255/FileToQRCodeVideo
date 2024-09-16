import tkinter as tk # for ease of access in selecting files for processing
from tkinter import filedialog # for ease of access in selecting files for processing

def checkBinary(file1Binary, file2Binary):
    if file1Binary == file2Binary:
        return True
    else:
        return False
    

def main():
    # get file 1
    root = tk.Tk()
    root.withdraw()
    # Open a file dialog to select the file
    file_path1 = filedialog.askopenfilename(title="Select FILE 1")
    if not file_path1:
        print("No file selected. Exiting.")
        return
    
    # get file 2
    root2 = tk.Tk()
    root2.withdraw()
    # Open a file dialog to select the file
    file_path2 = filedialog.askopenfilename(title="Select FILE 2")
    if not file_path2:
        print("No file selected. Exiting.")
        return
    
    #get first file as binary
    with open(file_path1, 'rb') as file:
        file1Binary = file.read()

    #get second file as binary
    with open(file_path2, 'rb') as file:
        file2Binary = file.read()

    #check integrity
    if checkBinary(file1Binary, file2Binary):
        print("Files are the same")
    else:
        print("Files DIFFERENT!")
        print(file1Binary)
        print("")
        print(file2Binary)

main()
    