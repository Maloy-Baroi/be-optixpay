import base64
import datetime
from django.conf import settings
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def load_private_key():
    """Load the merchant's private key from a PEM file."""
    with open(settings.NAGAD_MERCHANT_PRIVATE_KEY, "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,  # If your key is encrypted, provide the passphrase here
            backend=default_backend()
        )
    return private_key


def load_public_key():
    """Load the Nagad RSA public key from a PEM file."""
    with open(settings.NAGAD_MERCHANT_PUBLIC_KEY, "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )
    return public_key


def encrypt_sensitive_data(sensitive_data):
    """Encrypt the sensitive data using Nagad's public key."""
    public_key = load_public_key()
    encrypted_data = public_key.encrypt(
        sensitive_data.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    data = base64.b64encode(encrypted_data).decode('utf-8')
    print("Encrypted data: {}".format(data))
    return data


def sign_sensitive_data(sensitive_data):
    """Sign the sensitive data using merchant's private key."""
    private_key = load_private_key()
    signature = private_key.sign(
        sensitive_data.encode('utf-8'),
        padding.PKCS1v15(),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode('utf-8')


def get_current_datetime():
    """Get the current date and time in the format required by the API."""
    return datetime.datetime.now().strftime('%Y%m%d%H%M%S')
