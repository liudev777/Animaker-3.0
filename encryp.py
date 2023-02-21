from cryptography.fernet import Fernet
import os
import dotenv

dotenv.load_dotenv()
K = Fernet(os.environ['CRYPTO_KEY'].encode())

def encrypt(token):
    token = K.encrypt(token.encode()).decode()
    return token

def decrypt(encrypted_token):
    return K.decrypt(encrypted_token)

