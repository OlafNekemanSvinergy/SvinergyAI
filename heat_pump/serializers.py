from rest_framework import serializers
from heat_pump.models import Connection


class ConnectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Connection
        fields = ['id', 'brand', 'device_id',  'access_token', 'refresh_token', 'valid_until', 'expires_in', 'active']
