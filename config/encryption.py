import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES


KEY = '12345678901234567890123456789012'
salt = "anySaltYouCanUseOfOn"

block_size = 16
pad = lambda s: s + (block_size - len(s) % block_size) * chr(block_size - len(s) % block_size)
unpad = lambda s: s[0:-ord(s[-1:])]
iv = Random.new().read(AES.block_size)  # Random IV


def get_private_key():
    return hashlib.pbkdf2_hmac('SHA256', KEY.encode(), salt.encode(), 65536, 32)


def encrypt(data):
    private_key = get_private_key()
    data = pad(data)
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    cipher_bytes = base64.b64encode(iv + cipher.encrypt(data.encode("utf8")))
    return bytes.decode(cipher_bytes)


def decrypt(data):
    private_key = get_private_key()
    cipher_text = base64.b64decode(data)
    iv = cipher_text[:AES.block_size]
    cipher = AES.new(private_key, AES.MODE_CBC, iv)
    plain_bytes = unpad(cipher.decrypt(cipher_text[block_size:]))
    return bytes.decode(plain_bytes)
