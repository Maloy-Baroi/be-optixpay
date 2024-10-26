import json

import requests
from django.conf import settings
from services.nagad import encrypt_sensitive_data, sign_sensitive_data, get_current_datetime
import secrets


def generate_challenge():
    """Generates a secure random string for the challenge."""
    return secrets.token_hex(20)  # Generates a 40-character hex string


class NagadAPIService:
    def __init__(self):
        self.base_url = settings.NAGAD_BASE_URL
        self.merchant_id = settings.NAGAD_MERCHANT_ID
        self.merchant_mobile_number = settings.NAGAD_MERCHANT_MOBILE_NUMBER

    def initialize_payment(self, order_id, amount):
        """Initialize the payment session."""
        sensitive_data = {
            "merchantId": self.merchant_id,
            "dateTime": get_current_datetime(),
            "orderId": order_id,
            "challenge": generate_challenge()  # generate a secure random string
        }

        # Convert the sensitive data to a JSON string before encrypting
        sensitive_data_str = json.dumps(sensitive_data)

        encrypted_data = encrypt_sensitive_data(sensitive_data_str)
        print("Encrypted Data:", format(encrypted_data))
        signature = sign_sensitive_data(sensitive_data_str)

        print(f"signature: {signature}")

        payload = {
            # "accountNumber": self.merchant_mobile_number,  # optional
            "dateTime": get_current_datetime(),
            "sensitiveData": encrypted_data,
            "signature": signature,
        }

        headers = {
            "user-agent": "OptixPay/1.0 (Django REST Framework)",
            "x-km-api-version": "v-0.2.0",
            "x-km-ip-v4": "192.168.0.102",
            "accept-encoding": "gzip",
            "host": "sandbox-ssl.mynagad.com",
            "content-type": "application/json; charset=utf-8",
            "x-km-client-type": "PC_WEB"
        }

        response = requests.post(
            f"{self.base_url}/check-out/initialize/{self.merchant_id}/{order_id}",
            json=payload,
            headers=headers
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"Error: Received status code {response.status_code}")
            print(f"Response text: {response.text}")
            return {"error": f"Failed with status code {response.status_code}"}

    def complete_payment(self, payment_ref_id, amount):
        """Complete the payment by sending order details."""
        sensitive_data = {
            "merchantId": self.merchant_id,
            "orderId": "order123",
            "amount": amount,
            "currencyCode": "050",  # BDT
            "challenge": "challenge_from_initialization_response"
        }

        encrypted_data = encrypt_sensitive_data(str(sensitive_data))
        signature = sign_sensitive_data(str(sensitive_data))

        payload = {
            "sensitiveData": encrypted_data,
            "signature": signature,
            "merchantCallbackURL": settings.NAGAD_CALLBACK_URL,
            "additionalMerchantInfo": {
                "productName": "T-shirt",
                "productCount": 1
            }
        }

        response = requests.post(
            f"{self.base_url}check-out/complete/{payment_ref_id}",
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        return response.json()

    def check_payment_status(self, payment_ref_id):
        """Check the status of a payment."""
        response = requests.get(
            f"{self.base_url}verify/payment/{payment_ref_id}",
            headers={"Content-Type": "application/json"}
        )
        return response.json()
