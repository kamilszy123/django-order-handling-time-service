from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Account
from integrations.allegro.auth import exchange_code_for_token, AllegroAuthError


class AllegroCallbackView(APIView):
    def get(self, request):
        code = request.GET.get('code')

        if not code:
            return Response({"error": "no code provided"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            account, _ = Account.objects.get_or_create(name="Allegro")

            exchange_code_for_token(account, code)

            return Response({"status": "connected"}, status=status.HTTP_200_OK)
        except AllegroAuthError as e:
            return Response({"error": str(e)}, status=e.status_code or status.HTTP_400_BAD_REQUEST)
