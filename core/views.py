import pyotp
from django.shortcuts import render
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, UpdateAPIView, ListAPIView

from core.models import User, QrCode
from core.serializers import UserCreateSerializer, RetrieveUserSerializer, QrCodeCreateSerializer, RetrieveQrCodeSerializer
from core.utils import get_qrcode


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class RetrieveUserView(RetrieveUpdateDestroyAPIView):
    model = User
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RetrieveUserSerializer
    lookup_field = 'username'

    def get_queryset(self) -> User:
        return User.objects.all()

    # def get_object(self) -> User:
    #     return User.objects.all()

class RetrieveListUserView(ListAPIView):
    model = User
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RetrieveUserSerializer

    def get_queryset(self) -> User:
        return User.objects.all()


class CreateQrCodeView(CreateAPIView):
    queryset = QrCode.objects.all()
    serializer_class = QrCodeCreateSerializer
    lookup_field = 'user'
    lookup_url_kwarg = 'username'

    def perform_create(self, serializer):
        user = self.request.user
        key = pyotp.random_base32()
        qr_code = get_qrcode(user, key)
        serializer.save(key=key, qr_code_image=qr_code, user=user)
        print(f'user: {user.password}, key: {key}')


class RetrieveQrCodeView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = RetrieveQrCodeSerializer
    lookup_field = 'username'

    # def get_queryset(self) -> User:
    #     print(f'user: {self.request.user.id}')
    #     return User.objects.all()

    # def get(self, request, *args, **kwargs):
    #     user = User.objects.get(username=kwargs["username"])
    #     qr_code = QrCode.objects.filter(user=user).first()
    #     print(f'user: {user.id}, qrcode: {qr_code.id}, kwargs: {kwargs}')
    #     return qr_code
