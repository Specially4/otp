from django.contrib.auth.password_validation import validate_password
from django.core.files.base import ContentFile
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.validators import UniqueValidator

from core.models import User, QrCode


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        max_length=100,
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )
    password = serializers.CharField(min_length=1, write_only=True, validators=[validate_password])
    password_repeat = serializers.CharField(min_length=1, write_only=True, validators=[validate_password])

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
            'password',
            'password_repeat'
        ]

    def validate(self, attrs: dict) -> dict:
        """
        Переопределил пустой validate для проверки пароля, так же достаю и удаляю password_repeat.
        """
        password_repeat = attrs.pop('password_repeat', None)
        password = attrs.get('password')

        if password_repeat != password:
            raise ValidationError('Passwords do not match')
        return attrs

    def create(self, validated_data: dict) -> User:
        user = User.objects.create_user(**validated_data)
        return user


class RetrieveUserSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ]
    )

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'email',
            'first_name',
            'last_name',
        ]


# class RetrieveQrCodeSerializer(serializers.ModelSerializer):
#     qr_codes = serializers.SlugRelatedField(
#         many=True,
#         read_only=True,
#         slug_field='image_url',
#     )
#     # qr_codes = serializers.StringRelatedField(many=True, source='qr_code_image')

#     class Meta:
#         model = User
#         fields = ('username', 'email', 'qr_codes')


class RetrieveQrCodeSerializer(serializers.ModelSerializer):
    # qr_codes = serializers.SlugRelatedField(
    #     many=True,
    #     read_only=True,
    #     slug_field='image_url',
    # )
    # qr_codes = serializers.StringRelatedField(many=True, source='qr_code_image')
    user = serializers.CharField(source='user__username')

    class Meta:
        model = QrCode
        fields = '__all__'


class QrCodeCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = QrCode
        fields = []

    def save(self, **kwargs):
        qrcode = QrCode(user=kwargs['user'], key=kwargs['key'])
        qrcode.qr_code_image.save(f'qr_{kwargs["username"]}.png', ContentFile(kwargs['qr_code_image'].getvalue()), save=False)
        qrcode.save()
