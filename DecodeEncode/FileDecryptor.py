from cryptography.hazmat.primitives import hashes, padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class FileDecryptor:
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

    def decrypt_file(self, file_path):
        key = self._derive_key()

        # Read the encrypted file content
        with open(file_path, 'rb') as f:
            iv = f.read(16)  # The first 16 bytes are the IV
            encrypted_data = f.read()  # The rest is the encrypted data

        # Create a Cipher object using AES decryption with CBC mode
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=self.backend)
        decryptor = cipher.decryptor()

        # Decrypt the data
        padded_data = decryptor.update(encrypted_data) + decryptor.finalize()

        # Remove padding
        unpadder = padding.PKCS7(algorithms.AES.block_size).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()

        # Write the decrypted data to a new file
        decrypted_file_path = file_path[:-4]  # Remove the '.enc' extension
        with open(decrypted_file_path, 'wb') as f:
            f.write(data)

        print(f"File decrypted and saved as {decrypted_file_path}")

'''# Example usage
if __name__ == "__main__":
    password = 'your_password_here'
    salt = b'your_salt_here'  # Salt must be a bytes object
    file_path = 'path/to/your/encrypted_file.enc'

    decryptor = FileDecryptor(password, salt)
    decryptor.decrypt_file(file_path)
'''