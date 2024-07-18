from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from core import views


urlpatterns = [
    # path('users', views.RetrieveListUserView.as_view(), name='users'),
    # path('users/signup', views.CreateUserView.as_view(), name='signup'),
    # path('user/<str:username>/', views.RetrieveUserView.as_view(), name='user'),
    # Создание и просмотр QR-кода
    # path('user/<str:username>/qr-codes', views.RetrieveQrCodeView.as_view(), name='qr-codes'),
    path('user/<str:username>/qrcode', views.get_qrcode, name='qrcode'),
    path('user/<str:username>/qrcode/create', views.create_user_qrcode, name='create_qrcode'),
    path('user/<str:username>/qrcode/check', views.check_qrcode, name='check_qrcode'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
