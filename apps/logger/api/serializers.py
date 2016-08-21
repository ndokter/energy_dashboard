from rest_framework import serializers


class ReadingSerializer(serializers.Serializer):
    datetime = serializers.CharField(source='datetime__aggregate')
    value = serializers.FloatField(source='value_increment__sum')
    costs = serializers.FloatField(source='costs__sum')
