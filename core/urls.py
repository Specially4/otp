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
    path('user/<str:username>/qr_codes', views.get_qr_code, name='qr-codes'),
    path('user/<str:username>/create_qr_code', views.create_qr_code, name='create_qr_code'),
    # path('qr-codes/<int:pk>/', views.QrCodeDetailView.as_view(), name='qr-code-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
