from rest_framework import serializers


class CheckboxResponse(serializers.Serializer):
    choosed = serializers.ListField(required=True)
    button = serializers.ListField(required=True)