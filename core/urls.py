from django.urls import path

from core import views

urlpatterns = [
    path('users', views.RetrieveListUserView.as_view(), name='users'),
    path('users/signup', views.CreateUserView.as_view(), name='signup'),
    path('user/<str:username>/', views.RetrieveUserView.as_view(), name='user'),
    # Создание и просмотр QR-кода
    path('user/<str:username>/qr-codes', views.RetrieveQrCodeView.as_view(), name='qr-codes'),
    path('user/<str:username>/qr-codes/create/', views.CreateQrCodeView.as_view(), name='qr-code'),
    # path('qr-codes/<int:pk>/', views.QrCodeDetailView.as_view(), name='qr-code-detail'),
]
