from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from integrations.allegro.exceptions import AllegroError
from integrations.allegro.service import get_offers
from .models import Account, HandlingTimeConfig
from integrations.allegro.auth import exchange_code_for_token
from .serializers import HandlingTimeConfigSerializer, HandlingTimeBulkSerializer, HandlingTimeConfigListSerializer


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


class HandlingTimeConfigView(APIView):
    def get(self,request):
        config = HandlingTimeConfig.objects.all()

        serializer = HandlingTimeConfigListSerializer(config, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def post(self, request):
        serializer = HandlingTimeConfigSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        offer_id = serializer.validated_data["offer_id"]
        target_date = serializer.validated_data["target_date"]

        account = Account.objects.first()
        if not account:
            return Response(
                {"error": "No account configured"},
                status=status.HTTP_400_BAD_REQUEST
            )
        _, was_created = HandlingTimeConfig.objects.update_or_create(
            offer_id=offer_id,
            defaults={
                "account": account,
                "target_date": target_date
            }
        )

        return Response(
            {
                "status": "created" if was_created else "updated",
                "offer_id": offer_id,
                "target_date": target_date
            },
            status=status.HTTP_200_OK
        )


class HandlingTimeBulkConfigView(APIView):
    def post(self, request):
        serializer = HandlingTimeBulkSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        target_date = serializer.validated_data["target_date"]
        account = Account.objects.first()
        if not account:
            return Response(
                {"error": "No account configured"},
                status=status.HTTP_400_BAD_REQUEST
            )
        response = get_offers(account)

        offers = response.get("offers", [])
        offer_ids = [offer["id"] for offer in offers]

        created = 0
        updated = 0

        for offer_id in offer_ids:
            _, was_created = HandlingTimeConfig.objects.update_or_create(
                offer_id=offer_id,
                defaults={
                    "account": account,
                    "target_date": target_date
                }
            )
            if was_created:
                created += 1
            else:
                updated += 1

        return Response(
            {
                "status": "ok",
                "created": created,
                "updated": updated
            },
            status=status.HTTP_200_OK
        )