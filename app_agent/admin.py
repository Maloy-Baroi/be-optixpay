from django.contrib import admin

from app_agent.models.agent import PaymentProvider, PaymentAggregatorAgent

# Register your models here.
admin.site.register(PaymentProvider)
admin.site.register(PaymentAggregatorAgent)

