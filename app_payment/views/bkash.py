import json

from rest_framework.response import Response
from rest_framework.views import APIView
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# views.py
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from app_merchant.models.merchant import Merchant
from app_payment.models.payment import Payment
from services.bkash_create_sandbox import bkash_create_sandbox
from services.invoice_generator import generate_invoice_number


class DepositBKashPayView(APIView):
    def post(self, request):
        app_key = request.data.get('app_key')
        secret_key = request.data.get('secret_key')
        merchant = request.data.get('merchant')

        print(f"app_key: {app_key}, \nsecret_key: {secret_key}, \nmerchant: {merchant}")

        merchant = Merchant.objects.get(id=int(merchant))

        username = request.data.get('username')
        password = request.data.get('password')
        payment_amount = request.data.get('payment_amount')
        payment_method = request.data.get('payment_method')
        payment_currency = request.data.get('payment_currency')
        # Define the headers
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json",
            "username": username,
            "password": password
        }

        # Define the body
        data = {
            "app_key": app_key,
            "app_secret": secret_key
        }

        try:
            # Make the request to the external API using requests
            response = requests.post(
                "https://tokenized.sandbox.bka.sh/v1.2.0-beta/tokenized/checkout/token/grant",
                json=data,
                headers=headers
            )

            # Check if the response is successful
            if response.status_code == 200:
                response_json = response.json()
                response_json_dictionary = dict(response_json)
                id_token = response_json_dictionary['id_token']
                if id_token:
                    # sandbox = bkash_create_sandbox(
                    #     call_back_path="http://localhost:3000/",
                    #     amount=payment_amount,
                    #     currency=payment_currency,
                    #     invoice_number=invoice_number,
                    #     merchant_id=username,
                    #     id_token=id_token,
                    #     x_app_key=app_key,
                    #     username=username
                    # )

                    create_payment = Payment(merchant=merchant,
                                             amount=payment_amount,
                                             currency=payment_currency,
                                             paymentMethod=payment_method,
                                             created_by=merchant.user,
                                             updated_by=merchant.user)
                    create_payment.save()

                    return Response({"message": "Auth Token Found!",
                                     "data": {"id_token": id_token, "payment_id": create_payment.id}},
                                    status=status.HTTP_200_OK)
            elif response.status_code == 401:
                return Response({"error": "Unauthorized: Invalid credentials!"}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response({"error": response.json().get('message', 'An error occurred')},
                                status=response.status_code)

        except requests.exceptions.RequestException as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class BkashPaymentInitiateAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Initiates a bKash tokenized payment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'payer_reference': openapi.Schema(type=openapi.TYPE_STRING, description='Payer reference number'),
                'callback_url': openapi.Schema(type=openapi.TYPE_STRING,
                                               description='Callback URL for payment updates'),
                'merchant_association_info': openapi.Schema(type=openapi.TYPE_STRING,
                                                            description='Merchant association info'),
                'amount': openapi.Schema(type=openapi.TYPE_STRING, description='Amount to be paid'),
                'currency': openapi.Schema(type=openapi.TYPE_STRING, description='Currency code'),
                'intent': openapi.Schema(type=openapi.TYPE_STRING, description='Transaction intent'),
            },
            required=['payer_reference', 'amount']
        ),
        responses={200: 'Payment initiation successful', 400: 'Authentication failed'}
    )
    def post(self, request):
        # Extract individual fields from the request data
        token = request.data.get('id_token')  # Extract id_token from request
        x_app_key = request.data.get("x_app_key", "0vWQuCRGiUX7EPVjQDr0EUAYtc")  # Default value if not present
        payer_reference = request.data.get('payer_reference', "")  # Default payer reference
        callback_url = request.data.get("callback_url", "http://localhost:3000/call-back/")  # Default callback URL
        merchant_association_info = request.data.get('merchant_association_info',
                                                     "MI05MID54RF091234560ne")  # Default info
        amount = str(request.data.get('amount', "1"))  # Convert amount to string and default to "1"
        currency = request.data.get('currency', "BDT")  # Default currency is BDT
        intent = request.data.get('intent', "authorization")  # Default intent
        invoice_number = generate_invoice_number()  # Generate the unique invoice number

        if token:
            url = f"{settings.BKASH_BASE_URL}/tokenized/checkout/create"
            headers = {
                'Authorization': f'{token}',
                'Content-Type': 'application/json',
                'Accept': 'application/json',
                'x-app-key': x_app_key
            }
            data = {
                "mode": "0011",
                "payerReference": payer_reference,
                "callbackURL": callback_url,
                "merchantAssociationInfo": merchant_association_info,
                "amount": amount,
                "currency": currency,
                "intent": intent,
                "merchantInvoiceNumber": invoice_number
            }

            # Make the POST request
            response = requests.post(url, json=data, headers=headers)

            # Handle the response based on status code
            if response.status_code == 200:
                return Response(
                    {
                        "message": "Start Depositing",
                        "data": response.json(),
                        "id_token": token,
                        "x_app_key": x_app_key
                    },
                    status=200
                )
            return Response(response.json(), status=response.status_code)

        return Response({"error": "Could not authenticate"}, status=400)


class BkashPaymentExecuteAPIView(APIView):
    @swagger_auto_schema(
        operation_description="Executes a previously initiated bKash payment",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'payment_id': openapi.Schema(type=openapi.TYPE_STRING, description='Payment ID to execute')
            },
            required=['payment_id']
        ),
        responses={200: 'Payment execution successful', 400: 'Authentication failed'}
    )
    def post(self, request):
        id_token = request.data.get('id_token')
        x_app_key = request.data.get('x_app_key')
        pay_model_id = request.data.get('pay_model_id')
        if id_token:
            payment_id = request.data.get('payment_id')
            payload = json.dumps({
                "paymentID": payment_id
            })
            url = f"{settings.BKASH_BASE_URL}/tokenized/checkout/execute"
            headers = {
                'Authorization': f'{id_token}',
                'Accept': 'application/json',
                'x-app-key': x_app_key,
            }

            payment_obj = Payment.objects.get(id=int(pay_model_id))

            response = requests.request("POST", url, headers=headers, data=payload)

            if response.status_code == 200 and response.json().get('transactionStatus') and response.json().get('transactionStatus') == 'Authorized':
                payment_obj.paymentID = response.json().get('paymentID')
                payment_obj.trxID = response.json().get('trxID')
                payment_obj.intent = response.json().get('intent')
                payment_obj.merchantInvoiceNumber = response.json().get('merchantInvoiceNumber')
                payment_obj.payerType = response.json().get('payerType')
                payment_obj.payerReference = response.json().get('payerReference')
                payment_obj.customerMsisdn = response.json().get('customerMsisdn')
                payment_obj.payerAccount = response.json().get('payerAccount')
                payment_obj.status = response.json().get('statusMessage').lower()

                payment_obj.save()

                return Response({"data": response.json()}, status=status.HTTP_200_OK)
            else:
                payment_obj.status = response.json().get('statusMessage')

                payment_obj.save()
                return Response({"message": "Payment is unsuccessful"}, status=status.HTTP_406_NOT_ACCEPTABLE)
        return Response({"error": "Could not authenticate"}, status=status.HTTP_400_BAD_REQUEST)
