from django.urls import path

from core import views

urlpatterns = [
    path('users', views.RetrieveUserView.as_view(), name='users'),
    path('users/signup', views.CreateUserView.as_view(), name='signup'),
    # Создание и просмотр QR-кода
    path('qr-codes', views.RetrieveQrCodeView.as_view(), name='qr-codes'),
    path('qr-codes/create/', views.CreateQrCodeView.as_view(), name='qr-code'),
    # path('qr-codes/<int:pk>/', views.QrCodeDetailView.as_view(), name='qr-code-detail'),
]
