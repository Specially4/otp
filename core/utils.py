import pyotp
import qrcode
import time

from .models import User


def get_uri(name: str, key: str, issuer_name: str | None = 'TEST_OTP'):
    uri = pyotp.totp.TOTP(key).provisioning_uri(name=name, issuer_name=issuer_name)
    #encrypted_uri = encrypted_uri(uri)
    return uri

def get_qrcode(user: User, key: str) -> str:
    uri = get_uri(name=user.username, key=key)
    path = f'media/qr_{user.username}.png'
    qrcode.make(uri).save(path)
    return path
