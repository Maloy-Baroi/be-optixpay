# utils/nagad.py
import requests
from django.conf import settings

def initiate_payment(amount, order_id):
    url = f"{settings.NAGAD_BASE_URL}/checkout/initiate"
    payload = {
        "merchant_id": settings.NAGAD_MERCHANT_ID,
        "order_id": order_id,
        "amount": amount,
        "callback_url": settings.NAGAD_CALLBACK_URL,
    }
    headers = {
        "Authorization": f"Bearer {settings.NAGAD_MERCHANT_SECRET}",
        "Content-Type": "application/json",
    }
    response = requests.post(url, json=payload, headers=headers)
    return response.json()

def verify_payment(payment_id):
    url = f"{settings.NAGAD_BASE_URL}/checkout/verify/{payment_id}"
    headers = {
        "Authorization": f"Bearer {settings.NAGAD_MERCHANT_SECRET}",
        "Content-Type": "application/json",
    }
    response = requests.get(url, headers=headers)
    return response.json()
