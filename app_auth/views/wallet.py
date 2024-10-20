from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from app_auth.models.wallet import Wallet
from app_auth.serializers.wallet import WalletSerializer

class WalletViewSet(viewsets.ModelViewSet):
    queryset = Wallet.objects.all()
    serializer_class = WalletSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Optionally filter wallets by the logged-in user
        return Wallet.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Automatically associate the wallet with the logged-in user
        serializer.save(user=self.request.user)
