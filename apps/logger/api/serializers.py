from rest_framework import serializers


class ReadingSerializer(serializers.Serializer):
    value = serializers.FloatField(source='value_increment__sum')
    datetime = serializers.CharField(source='datetime__aggregate')


class ElectricityReadingSerializer(ReadingSerializer):
    tariff = serializers.IntegerField()
