from django.contrib.auth.models import User
from rest_framework import serializers
from .models import AdoptionRequest, Pet

class PetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"

class AdoptionRequestSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source="user.username")

    class Meta:
        model = AdoptionRequest
        fields = [
            "id", "user", "pet", "phone", "address", "reason",
            "previous_pet_experience", "message", "status", "created_at"
        ]
        read_only_fields = ["status", "created_at"]

    def validate(self, attrs):
        request = self.context["request"]
        pet = attrs.get("pet")
        if pet.status != "Available":
            raise serializers.ValidationError("Only available pets can be adopted.")
        if AdoptionRequest.objects.filter(
            user=request.user, pet=pet, status__in=["Pending", "Approved"]
        ).exists():
            raise serializers.ValidationError("You already have an active request for this pet.")
        return attrs

    def create(self, validated_data):
        return AdoptionRequest.objects.create(
            user=self.context["request"].user, **validated_data
        )
