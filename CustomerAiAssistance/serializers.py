from rest_framework import serializers

class QuerySerializer(serializers.Serializer):
    query = serializers.CharField(max_length=2000)
