from rest_framework import serializers


class HandlingTimeConfigSerializer(serializers.Serializer):
    offer_id = serializers.CharField()
    target_date = serializers.DateField()

class HandlingTimeBulkSerializer(serializers.Serializer):
    target_date = serializers.DateField()