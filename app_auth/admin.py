from django.contrib import admin
from app_auth.models import user, wallet, agent_profile


# Register your models here.
admin.site.register(user.CustomUser)
admin.site.register(agent_profile.AgentProfile)
admin.site.register(wallet.Wallet)
