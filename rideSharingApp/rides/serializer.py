from rest_framework_mongoengine import serializers
from .models import RideRequest
# from rest_framework import serializers as sr

# class PendingRideRequestSerialezer(serializers.Serializer):
#     class Meta:
#         model=RideRequest
#         des
#         fields = "__all__"

class RideRequestSerializer(serializers.DocumentSerializer):
    class Meta:
        model=RideRequest
        fields = "__all__" 


