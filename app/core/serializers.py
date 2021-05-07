from rest_framework import serializers

from app.core.models import City, Airport


class AirportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Airport
        fields = ('code', 'name')


class SearchSerializer(serializers.ModelSerializer):
    airport = serializers.SerializerMethodField()
    city = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ('city', 'airport')
        read_only_fields = fields

    def get_city(self, obj):
        return {
            'code': obj.code,
            'name': obj.name
        }

    def get_airport(self, obj):
        airports = obj.airports.all()
        if airports.exists():
            ser = AirportSerializer(airports, many=True)
            return ser.data
        return []
