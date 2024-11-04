import requests
import json

url = "https://tokenized.pay.bka.sh/v1.2.0-beta/tokenized/checkout/create"

def bkash_create_sandbox(call_back_path, amount, currency, invoice_number, merchant_id, id_token, x_app_key, username):
    try:
        payload = json.dumps({
        "mode": "0011",
        "payerReference": username,
        "callbackURL": call_back_path,
        "merchantAssociationInfo": merchant_id,
        "amount": str(amount) if amount else "1",
        "currency": currency,
        "intent": "authorization",
        "merchantInvoiceNumber": invoice_number
        })
        
        headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': id_token,
        'x-app-key': x_app_key
        }
        
        response = requests.request("POST", url, headers=headers, data=payload)
        print(response.json())
        
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except Exception as e:
        raise str(e)
    