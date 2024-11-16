import requests
import json
import socket
import rsa
import random
import base64
import datetime
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization


class Nagad:
    def __init__(self, credentials):
        self.client = requests.Session()
        self.credentials = credentials
        self.additional_merchant_info = {}

    def set_additional_merchant_info(self, additional_info):
        self.additional_merchant_info = additional_info

    def regular_payment(self, order_id, amount):
        print(f"Is Sandbox: {self.credentials['isSandbox']}")
        base_url = "https://sandbox-ssl.mynagad.com" if self.credentials['isSandbox'] else "https://api.mynagad.com"
        kpg_default_seed = f"nagad-dfs-service-ltd{int(datetime.datetime.now().timestamp() * 1000)}"

        # Load and convert the public key using cryptography
        public_key_obj = serialization.load_pem_public_key(
            self.credentials['pgPublicKey'].encode(),
            backend=default_backend()
        )
        public_key = rsa.PublicKey.load_pkcs1(
            public_key_obj.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.PKCS1
            )
        )

        # Load and convert the private key using cryptography
        private_key_obj = serialization.load_pem_private_key(
            self.credentials['merchantPrivateKey'].encode(),
            password=None,
            backend=default_backend()
        )
        private_key = rsa.PrivateKey.load_pkcs1(
            private_key_obj.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )
        )

        datetime_now = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
        random_challenge = self.generate_random_string(20, kpg_default_seed.encode())

        raw_data = {
            'merchantId': self.credentials['merchantID'],
            'orderId': order_id,
            'datetime': datetime_now,
            'challenge': random_challenge
        }

        # Encrypt raw data with the public key
        raw_data_to_be_encrypted = json.dumps(raw_data)
        sensitive_data = base64.b64encode(rsa.encrypt(raw_data_to_be_encrypted.encode(), public_key)).decode()

        # Sign the data with the private key
        signature = base64.b64encode(rsa.sign(raw_data_to_be_encrypted.encode(), private_key, 'SHA-256')).decode()

        # Get IP address
        ip_address = self.get_ip_address()

        headers = {
            'Content-Type': 'application/json',
            'X-KM-IP-V4': ip_address,
            'X-KM-Client-Type': 'MOBILE_APP',
            'X-KM-Api-Version': 'v-0.2.0',
        }

        # API call to initialize checkout
        try:
            response = self.client.post(
                f"{base_url}/api/dfs/check-out/initialize/{self.credentials['merchantID']}/{order_id}",
                headers=headers,
                json={
                    'dateTime': datetime_now,
                    'sensitiveData': sensitive_data,
                    'signature': signature,
                }
            )
            print("Response: ", response.json())
        except requests.RequestException as e:
            raise Exception(f"Exception in Check Out Initialize API {e}")

        if response.status_code == 200:
            response_body = response.json()
            print(response_body.get('payment_url'))
            sensitive_data = response_body['sensitiveData']
            signature = response_body['signature']

            # Decrypt the response
            decrypted_data = rsa.decrypt(base64.b64decode(sensitive_data), private_key).decode()
            verified = rsa.verify(decrypted_data.encode(), base64.b64decode(signature), public_key)

            if verified:
                decrypted_data_body = json.loads(decrypted_data)
                challenge = decrypted_data_body['challenge']
                payment_reference_id = decrypted_data_body['paymentReferenceId']

                raw_data = {
                    'merchantId': self.credentials['merchantID'],
                    'orderId': str(order_id),
                    'currencyCode': '050',
                    'amount': amount,
                    'challenge': challenge
                }
                raw_data_to_be_encrypted = json.dumps(raw_data)
                sensitive_data = base64.b64encode(rsa.encrypt(raw_data_to_be_encrypted.encode(), public_key)).decode()
                signature = base64.b64encode(
                    rsa.sign(raw_data_to_be_encrypted.encode(), private_key, 'SHA-256')).decode()

                try:
                    complete_response = self.client.post(
                        f"{base_url}/api/dfs/check-out/complete/{payment_reference_id}",
                        headers=headers,
                        json={
                            'sensitiveData': sensitive_data,
                            'signature': signature,
                            'merchantCallbackURL': 'http://localhost:3000/call-back',
                            'additionalMerchantInfo': self.additional_merchant_info
                        }
                    )
                except requests.RequestException as e:
                    raise Exception(f"Exception in Check Out Complete API {e}")

                if complete_response.status_code == 200:
                    return complete_response.json()
                else:
                    raise Exception(
                        f"Check Out Complete API failed with status: {complete_response.status_code}, message: {complete_response.text}")
            else:
                raise Exception("Signature Verification Failed")
        else:
            raise Exception(
                f"Check Out Initialize API failed with status: {response.status_code}, message: {response.text}")

    def generate_random_string(self, size, seed):
        random.seed(int.from_bytes(seed, "big"))
        return ''.join(random.choices("0123456789abcdef", k=size))

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            s.connect(('10.254.254.254', 1))
            ip_address = s.getsockname()[0]
        except Exception:
            ip_address = '127.0.0.1'
        finally:
            s.close()
        return ip_address
