from cryptography.fernet import Fernet

def generate_key():
    """Generate and return a new encryption key."""
    key = Fernet.generate_key().decode('utf-8')
    # Replace URL-sensitive characters in the key
    return key.replace('=', '~')


def encrypt_message(message, key):
    """Encrypt a message using the provided key."""
    # Revert replaced characters in the key before using it
    key = key.replace('~', '=')
    fernet = Fernet(key)
    encrypted_message = fernet.encrypt(message.encode())
    # Replace URL-sensitive characters in the encrypted message
    return encrypted_message.decode('utf-8').replace('=', '~')


def decrypt_message(encrypted_message, key):
    """Decrypt an encrypted message using the provided key."""
    # Revert replaced characters in both the key and encrypted message
    key = key.replace('_', '=')
    encrypted_message = encrypted_message.replace('~', '=')
    fernet = Fernet(key)
    decrypted_message = fernet.decrypt(encrypted_message.encode()).decode()
    return decrypted_message
