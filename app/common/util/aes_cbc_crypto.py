from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64

class AesCbc128Crypto:
    keyValue = "9994561230777345"
    iv = b'\x01' * 16

    def __init__(self):
        self.secretKey = self.keyValue.encode('utf-8')
        self.ivSpec = self.iv
        self.cipher = AES.new(self.secretKey, AES.MODE_CBC, self.ivSpec)

    def encrypt(self, plain_text: str) -> str:
        if not plain_text:
            return ""

        cipher = AES.new(self.secretKey, AES.MODE_CBC, self.ivSpec)
        encrypted_bytes = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
        return base64.b64encode(encrypted_bytes).decode('utf-8')

    def decrypt(self, crypt_text: str) -> str:
        if not crypt_text:
            return ""

        cipher = AES.new(self.secretKey, AES.MODE_CBC, self.ivSpec)
        decrypted_bytes = unpad(cipher.decrypt(base64.b64decode(crypt_text)), AES.block_size)
        return decrypted_bytes.decode('utf-8')