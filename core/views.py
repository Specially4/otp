import pyotp
from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from rest_framework import permissions
from rest_framework.generics import (CreateAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView, UpdateAPIView,
                                     ListAPIView)

from core.models import User, QrCode
from core.serializers import (UserCreateSerializer, RetrieveUserSerializer, QrCodeCreateSerializer,
                              RetrieveQrCodeSerializer)
from core.utils import create_qrcode_image, check_token


# class CreateUserView(CreateAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserCreateSerializer


# class RetrieveUserView(RetrieveUpdateDestroyAPIView):
#     model = User
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = RetrieveUserSerializer
#     lookup_field = 'username'

#     def get_queryset(self) -> User:
#         return User.objects.all()

#     # def get_object(self) -> User:
#     #     return User.objects.all()


# class RetrieveListUserView(ListAPIView):
#     model = User
#     permission_classes = [permissions.IsAuthenticated]
#     serializer_class = RetrieveUserSerializer

#     def get_queryset(self) -> User:
#         return User.objects.all()


# class CreateQrCodeView(CreateAPIView):
#     queryset = QrCode.objects.all()
#     serializer_class = QrCodeCreateSerializer
#     lookup_field = 'user'
#     lookup_url_kwarg = 'username'

#     def perform_create(self, serializer):
#         user = self.request.user
#         key = pyotp.random_base32()
#         out = get_qrcode(user, key)
#         serializer.save(key=key, qr_code_image=out, user=user, username=user.username)
#         print(f'user: {user.password}, key: {key}')


# class RetrieveQrCodeView(RetrieveUpdateDestroyAPIView):
#     """
#     Отображение QR-кода конкретного пользователя и обновление/удаление QR-кода.
#     Надо до конца разобраться с реализацией, т.к не получается получить QR-код по username
#     Возможно стоит реализовать отдельно отображение и отдельно обновление QR-кода.
#     """
#     model = QrCode
#     serializer_class = RetrieveQrCodeSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     lookup_field = 'user'
#     lookup_url_kwarg = 'username'

#     def get_queryset(self) -> QrCode:
#         return QrCode.objects.filter(user=self.request.user)

# # class RetrieveQrCodeView(RetrieveUpdateDestroyAPIView):
# #     queryset = User.objects.all()
# #     serializer_class = RetrieveQrCodeSerializer
# #     lookup_field = 'username'

#     # def get_queryset(self) -> User:
#     #     print(f'user: {self.request.user.id}')
#     #     return User.objects.all()

#     # def get(self, request, *args, **kwargs):
#     #     user = User.objects.get(username=kwargs["username"])
#     #     qr_code = QrCode.objects.filter(user=user).first()
#     #     print(f'user: {user.id}, qrcode: {qr_code.id}, kwargs: {kwargs}')
#     #     return qr_code

def get_qrcode(request, username):
    """
    Отображение QR-кода конкретного пользователя.
    """
    user = User.objects.get(username=username)
    qrcode = QrCode.objects.filter(user=user).last()

    data = {
        'user': user,
        'qr_code': qrcode,
    }
    return render(request, 'qrcode.html', context=data)


def create_user_qrcode(request, username):
    """
    Создание QR-кода для конкретного пользователя и сохранение QR-кода в БД.
    """
    user = User.objects.get(username=username)
    key = pyotp.random_base32()
    out = create_qrcode_image(user, key)
    qrcode = QrCode(user=user, key=key)
    qrcode.qr_code_image.save(f'qr_{username}.png', ContentFile(out.getvalue()), save=False)
    qrcode.save()

    return redirect(get_qrcode, username=username)


def check_qrcode(request, username):
    """
    Проверка токена на валидность для конкретного пользователя.
    """
    user = User.objects.get(username=username)
    key = QrCode.objects.filter(user=user).last().key
    text = 'Нет доступа'
    if request.method == 'POST':
        token = request.POST.get('token')
        if check_token(key, token):
            text = "Success"
        else:
            text = "Bad Token"
    
    return render(request, 'check.html', {'status': text})
