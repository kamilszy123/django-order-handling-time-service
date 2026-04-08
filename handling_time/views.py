from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from integrations.allegro.exceptions import AllegroError
from integrations.allegro.service import get_offers, update_handling_time
from .models import Account
from integrations.allegro.auth import exchange_code_for_token


class AllegroCallbackView(APIView):
    def get(self, request):
        code = request.GET.get('code')

        if not code:
            return Response(
                {"error": "no code provided"},
                status=status.HTTP_400_BAD_REQUEST)
        try:
            account, _ = Account.objects.get_or_create(name="Allegro")

            exchange_code_for_token(account, code)

            return Response(
                {"status": "connected"},
                status=status.HTTP_200_OK
            )
        except AllegroError as e:
            return Response(
                {"error": str(e)},
                status=e.status_code or status.HTTP_400_BAD_REQUEST)


class AllegroGetOffersView(APIView):
    def get(self, request):
        try:
            account = Account.objects.first()
            if not account:
                return Response(
                    {"error": "No account configured"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            response = get_offers(account)
            return Response(
                {"offers": response},
                status=status.HTTP_200_OK
            )
        except AllegroError as e:
            return Response(
                {"error getting offers": str(e)},
                status=e.status_code or status.HTTP_502_BAD_GATEWAY
            )

