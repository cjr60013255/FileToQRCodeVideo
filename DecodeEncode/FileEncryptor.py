import os
from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class FileEncryptor:
    def __init__(self, password, salt):
        self.password = password
        self.salt = salt
        self.backend = default_backend()
        self.key_length = 32  # AES-256 requires a 32-byte (256-bit) key

    def _derive_key(self):
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=self.key_length,
            salt=self.salt,
            iterations=100000,
            backend=self.backend
        )
        return kdf.derive(self.password.encode())

    def encrypt_file(self, file_path):
        key = self._derive_key()

        # Generate a random IV (Initialization Vector)
        iv = os.urandom(16)

        # Create a Cipher object using AES encryption with CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        encryptor = cipher.encryptor()

        # Read the file data
        with open(file_path, 'rb') as f:
            file_data = f.read()

        # Pad the file data to be a multiple of the block size (16 bytes for AES)
        padder = padding.PKCS7(algorithms.AES.block_size).padder()
        padded_data = padder.update(file_data) + padder.finalize()

        # Encrypt the padded file data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()

        # Construct the encrypted file content (iv + encrypted_data)
        encrypted_file_content = iv + encrypted_data

        # Write the encrypted data to a new file
        encrypted_file_path = file_path + ".enc"
        with open(encrypted_file_path, 'wb') as f:
            f.write(encrypted_file_content)

        #print(f"File encrypted and saved as {encrypted_file_path}")

'''# Example usage
if __name__ == "__main__":
    password = 'your_password_here'
    salt = b'your_salt_here'  # Salt must be a bytes object
    file_path = 'path/to/your/file.txt'

    encryptor = FileEncryptor(password, salt)
    encryptor.encrypt_file(file_path)
'''