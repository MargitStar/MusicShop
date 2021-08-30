from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

User = get_user_model()


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("email", "username", "password")
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
        )
        user.set_password(validated_data["password"])
        user.save()

        group, created = Group.objects.get_or_create(name="User")
        group.user_set.add(user)
        return user
