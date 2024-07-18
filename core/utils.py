import io

import pyotp
import segno
import time

from .models import User


def get_uri(name: str, key: str, issuer_name: str | None = 'TEST_OTP') -> str:
    """
    Создание URI для OTP (One-Time Password) с использованием pyotp.
    """
    uri = pyotp.totp.TOTP(key).provisioning_uri(name=name, issuer_name=issuer_name)

    return uri


def create_qrcode_image(user: User, key: str):
    """
    Создание QR-кода с использованием pyotp и segno.
    И сохранение QR-кода в виде байтового потока. Такое решение принято т.к.
    не могу разобраться с сохранением QR-коде в БД.
    """
    uri = get_uri(name=user.username, key=key)
    qrcode = segno.make(uri)
    out = io.BytesIO()
    qrcode.save(out, kind='png', scale=5)

    return out


def check_token(key: str, token: str) -> bool:
    """
    Проверка токена на валидность с использованием pyotp.
    """
    totp = pyotp.TOTP(key)
    return totp.verify(token)
