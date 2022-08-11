from rest_framework import serializers
from demand_response.models import PriceItem


class PriceItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceItem
        fields = '__all__'
