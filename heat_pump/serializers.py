from rest_framework import serializers
from heat_pump.models import Connection


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['id', 'brand', 'access_token', 'refresh_token', 'valid_until', 'valid', 'active']
