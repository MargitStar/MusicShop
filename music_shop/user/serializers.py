from rest_framework import serializers

from user.models import CustomUser


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data["username"], email=validated_data["email"]
        )
        user.set_password(validated_data["password"])
        user.save()
        user.group = "User"
        user.save()
        return user
