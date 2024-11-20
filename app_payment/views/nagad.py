import os
import random

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings

from app_payment.models.payment import Payment
from app_payment.utils import Nagad

# from app_payment.utils import NagadAPIService
# Access the environment variables
credentials = {
    "merchantID": os.getenv("MERCHANT_ID"),
    "isSandbox": os.getenv("IS_SANDBOX") == "True",
    "pgPublicKey": f"-----BEGIN PUBLIC KEY-----\n{os.getenv('PG_PUBLIC_KEY')}\n-----END PUBLIC KEY-----",
    "merchantPrivateKey": f"-----BEGIN PRIVATE KEY-----\n{os.getenv('MERCHANT_PRIVATE_KEY')}\n-----END PRIVATE KEY-----"
}


# credentials = {
#     "merchantID": "687456515985399",
#     "isSandbox": True,
#     "pgPublicKey": f"-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAkwkhGZwsSbyjYH4hKmrlI5l3vWJVZE/kqIlaZ1yAk1vR2qYNPMwuSByov8AYixuKrAAzrCWD1ZLaWtizQimtloc/tp9IvNAfaxaOEzw/LTOIlPWj3umfi2d6D6Tpu75ACIMVmnzoccDbPUZAWu5KGvvZF3qTWJ/2OmhJ6u+tESysevWt7HtOC3kdipan47EZRmCbEuN16R7ylmqRsAYO0qtvCgft6+VyQi7gTeq4SMyGbakTjsJMlRjzQ8j9NxwxSd6Xb637eKzch7Gs3Nf2NnDXO9a3QDtWh9Jlr9JeNE3S61WHv2yDGDZCmXMTS6aeQpaCTl5xc27emRw6mTR9twIDAQAB\n-----END PUBLIC KEY-----",
#     "merchantPrivateKey": f"-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQCTCSEZnCxJvKNgfiEqauUjmXe9YlVkT+SoiVpnXICTW9Hapg08zC5IHKi/wBiLG4qsADOsJYPVktpa2LNCKa2Whz+2n0i80B9rFo4TPD8tM4iU9aPe6Z+LZ3oPpOm7vkAIgxWafOhxwNs9RkBa7koa+9kXepNYn/Y6aEnq760RLKx69a3se04LeR2KlqfjsRlGYJsS43XpHvKWapGwBg7Sq28KB+3r5XJCLuBN6rhIzIZtqROOwkyVGPNDyP03HDFJ3pdvrft4rNyHsazc1/Y2cNc71rdAO1aH0mWv0l40TdLrVYe/bIMYNkKZcxNLpp5CloJOXnFzbt6ZHDqZNH23AgMBAAECggEAEoL0ut+xp7rrKsvWaxu4K4o3zA0kSRPR6vIYAqlfuq21tvxu8DeYoBWTnUiXDnRyOgNwffzfIzVw7j0YHH1Y0HnIqLpXEwZ03iuhyYQtRAiX6oEel4L8RjXJ5UxS7QMf1rKCNsgBD8lDEOzWT1xu0gThKRaSlHbXLjVRERYJyP6RAkfknrskXeKw8cGWInC0Th77WyT7R/iykTT331fMgQVcyqClXHM1e3aSyw8jjnatGDfP0r9qhbBVkeQ8BgKE+v+agjHz8EKKYh8crU5HCG4wOIxMAVZxJUm4nwHedRlpIsO2X5zrHpclqJGLfwOoAyyzd9OpnN+dt31jqwVCoQKBgQDCA3LjXR8p055QjJwneXvzjD47q6pAU4S+tDOIF1dZbQUJ9QYvNraUzSMOtKkCzqJ9vRCm1ZqRygj71Fvx5J+Qcs0+5wu4pllfMJwcxwdY7+fUWTLAJsSU//hi6TF6rCpIrdZff5TmISDtz3RddIVPWmIzacEWmbI3bu959+62UQKBgQDCA1HNrKAWKYy2VC9P62g5lukFVElsSR9iBejw86GmsjJUk4T80eVdg5CauV8KeKL9NpoZTnqABpNjDzAMdm4D3Frs0NlsDJwyJG780f4G1j5Hdk+OTZsKwv4JFSwnC+mjHjoGm0S19O8pLK8gDtFp/5tzlL+QQvjLjjtsUXGJhwKBgQCBeLm3vxIn4H/68wrWUP0F16ZEPdf8239voGPvQtxY4icFsQ0yfsmzXX4ytx8+r1TComQ1YcCn3/LE07+UGmTdia8sdhVdYS2tF4xmq+9cS6UjEW+LyZNQd81zfHk3iyMgo1m3GzXrqVoHOXVHVJYOEZwNAVsI0QKceZy4gVs9MQKBgBQswjHwFImZcn93S6A065apgbvDIwt2oyPPV4TO4O1ztFYlLPwZW4+Y4c2lHyP4nYJVTjr5dTWg+WygpK93FUOjg3UC1sksmoWAUmZJ8++EEd/ehrFWkpvQ4RfSss+wpnAG8aPEO6XsPX57ng5oXBB4uxKO0kjPHg4U0UsXQQY7AoGAO+a07OPLNDMZpHvyToBIOh1ircp0Duul/Q595ouJ9C9CvNMAozm7Pz5t8H5klrJ6gSfqeMLi9owdMTvuXovOcuzqZwfw3f4tEjDxMuPIT+XLB/PHiyzN8Sw4GqGyggFlkF/Rk7Dj9GKEL6e4NkAIz3TMM31gz6aZi9h0+lGLUbw=\n-----END PRIVATE KEY-----"
# }


class StartPaymentView(APIView):
    def post(self, request):
        try:
            order_id = request.data.get('order_id')
            amount = request.data.get('amount')
            print(f"credentials: {credentials}")

            nagad = Nagad(credentials)
            print(f"nagad: {nagad}")
            payment_obj = Payment(
                paymentID=order_id,
                transaction_type="deposit",
                in_bdt=amount,
                paymentMethod="nagad",
                currency="BDT"
            )
            print("Payment Object", payment_obj)
            payment_obj.save()
            response = nagad.regular_payment(order_id=order_id, amount=amount)
            print("create response data:", response['callBackUrl'])
            return Response({"callBackUrl": response['callBackUrl']}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Response from exception: ", str(e))
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


class CompletePaymentView(APIView):
    def post(self, request):
        payment_id = request.data.get('payment_id')
        order_id = request.data.get('order_id')

        payment = Payment.objects.get(paymentID=order_id)
        payment.trxID = payment_id
        payment.status = "successful"
        payment.save()

        return Response({"message": "Successfully Paid"}, status=status.HTTP_200_OK)
#
# class CheckPaymentStatusView(APIView):
#     def get(self, request, payment_ref_id):
#         nagad_service = NagadAPIService()
#         result = nagad_service.check_payment_status(payment_ref_id)
#
#         return Response(result, status=status.HTTP_200_OK)
