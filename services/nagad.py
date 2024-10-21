# payments/services.py
import json
import uuid
import requests
from datetime import datetime
from django.conf import settings
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import serialization
import base64

class NagadPaymentService:

    def __init__(self):
        self.merchant_id = settings.NAGAD_PAYMENT['MERCHANT_ID']
        self.private_key = settings.NAGAD_PAYMENT['MERCHANT_PRIVATE_KEY']
        self.gateway_url = settings.NAGAD_PAYMENT['NAGAD_GATEWAY_URL']

    def generate_unique_payment_ref(self):
        """Generates a unique transaction reference"""
        return str(uuid.uuid4())

    def generate_signature(self, data):
        """Generate RSA signature using the merchant private key using `cryptography` library"""
        try:
            # Load private key from PEM format
            private_key = serialization.load_pem_private_key(
                self.private_key.encode('utf-8'),
                password=None,  # If your key is password-protected, provide the password here.
                backend=default_backend()
            )

            # Debugging step: Check the data
            print("Data to be signed:", data)

            # Create the signature
            signature = private_key.sign(
                data.encode('utf-8'),  # The data to sign
                padding.PKCS1v15(),  # Use PKCS#1 v1.5 padding
                hashes.SHA256()  # Use SHA-256 hash function
            )

            # Encode signature in Base64 to send to API
            signature_b64 = base64.b64encode(signature).decode('utf-8')

            print("Signature Generated:", signature_b64)  # For debugging
            return signature_b64

        except Exception as e:
            print(f"Error generating signature: {e}")

    def initiate_payment(self, amount, order_id):
        """Initiates a payment request to Nagad"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        unique_ref = self.generate_unique_payment_ref()

        payload = {
            "merchantId": self.merchant_id,
            "orderId": order_id,
            "currencyCode": "050",
            "amount": f"{amount:.2f}",
            "challenge": unique_ref,
            "timestamp": timestamp
        }

        print(payload)

        payload_json = json.dumps(payload)
        signature = self.generate_signature(payload_json)
        print("Signature Generated: " + signature)

        # Post request to Nagad
        headers = {
            'Content-Type': 'application/json',
            'signature': signature
        }

        response = requests.post(
            f"{self.gateway_url}/payment/initiate",
            headers=headers,
            data=payload_json
        )

        print("Nagad response: ", response.text)

        if response.status_code == 200:
            return response.json()  # Returns payment URL or error message
        else:
            return {"error": response.text}

    def confirm_payment(self, payment_ref):
        """Confirm the payment after user completes the payment on Nagad"""
        payload = {
            "paymentReferenceId": payment_ref,
            "merchantId": self.merchant_id
        }

        # Post confirmation request to Nagad
        response = requests.post(
            f"{self.gateway_url}/payment/confirm",
            json=payload
        )

        if response.status_code == 200:
            return response.json()  # Returns payment confirmation data
        else:
            return {"error": response.text}
