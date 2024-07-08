from django.shortcuts import render
from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from core.models import User, QrCode
from core.serializers import UserCreateSerializer, RetrieveUserSerializer, QrCodeCreateSerializer, RetrieveQrCodeSerializer
from core.utils import get_qrcode


class CreateUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class RetrieveUserView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = RetrieveUserSerializer

    def get_object(self) -> User:
        return self.request.user.all()


class CreateQrCodeView(CreateAPIView):
    queryset = QrCode.objects.all()
    serializer_class = QrCodeCreateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        qr_code = get_qrcode(user)
        serializer.save(user=user, key=qr_code['key'], qr_code_image=qr_code['path'])


class RetrieveQrCodeView(RetrieveUpdateDestroyAPIView):
    queryset = QrCode.objects.all()
    serializer_class = RetrieveQrCodeSerializer

    # def get_object(self) -> QrCode:
    #     return self.request.user.username
