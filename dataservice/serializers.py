
from rest_framework import serializers

from .models import Language

class LanduageSerializers(serializers.Serializer):
    name = serializers.CharField(max_length=100)
    favrate_word = serializers.CharField(max_length=100,null=True,blank=True)
    populations = serializers.PositiveIntegerField(blank=True,default=0)

    def create(self, validated_data):
        return Language.objects.create(**validated_data)