from rest_framework import serializers

from handling_time.models import HandlingTimeConfig


class HandlingTimeConfigSerializer(serializers.Serializer):
    offer_id = serializers.CharField()
    target_date = serializers.DateField()

class HandlingTimeBulkSerializer(serializers.Serializer):
    target_date = serializers.DateField()

class HandlingTimeConfigListSerializer(serializers.ModelSerializer):
    account = serializers.StringRelatedField()

    class Meta:
        model = HandlingTimeConfig
        fields = ["account", "offer_id", "target_date"]