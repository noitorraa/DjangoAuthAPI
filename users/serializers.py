from rest_framework import serializers
from django.contrib.auth import authenticate
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "password",
            "password_confirm",
        ]
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(_("Пароли не совпадают"))
        return attrs

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError(
                _("Пользователь с таким email уже существует")
            )
        return value

    def create(self, validated_data):
        validated_data.pop("password_confirm")
        user = CustomUser.objects.create_user(**validated_data)
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True, required=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if email and password:
            user = authenticate(username=email, password=password)
            if not user:
                raise serializers.ValidationError(_("Неверные учетные данные"))
            if not user.is_active:
                raise serializers.ValidationError(_("Аккаунт деактивирован"))
            attrs["user"] = user
        else:
            raise serializers.ValidationError(_("Необходимо указать email и пароль"))
        return attrs


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "middle_name",
            "date_joined",
        ]
        read_only_fields = ["id", "email", "date_joined"]


class UserUpdateSerializer(serializers.ModelSerializer):
    current_password = serializers.CharField(write_only=True, required=False)
    new_password = serializers.CharField(write_only=True, required=False, min_length=8)

    class Meta:
        model = CustomUser
        fields = [
            "first_name",
            "last_name",
            "middle_name",
            "current_password",
            "new_password",
        ]

    def validate(self, attrs):
        if "new_password" in attrs and "current_password" not in attrs:
            raise serializers.ValidationError(
                _("Для смены пароля необходим текущий пароль")
            )
        return attrs

    def update(self, instance, validated_data):
        current_password = validated_data.pop("current_password", None)
        new_password = validated_data.pop("new_password", None)

        if new_password and current_password:
            if not instance.check_password(current_password):
                raise serializers.ValidationError(_("Неверный текущий пароль"))
            instance.set_password(new_password)
            instance.save()

        # Обновляем остальные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
