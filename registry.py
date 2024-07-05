import pyotp
import qrcode
import time
import hashlib

from db.db import save_user, Person, search_user
from constants import SECRET
#from crypto import encrypted_uri, decrypted_uri

def get_uri(name: str, secret: str, issuer_name: str | None = None):
    uri = pyotp.totp.TOTP(secret).provisioning_uri(name=name, issuer_name=issuer_name)
    #encrypted_uri = encrypted_uri(uri)
    return uri

def get_qrcode(user: Person):
    uri = get_uri(name=user.name, secret=user.secret, issuer_name=user.issuer_name)
    qrcode.make(uri).save(f'qr {user.name}.png')
    print(f'QR code saved to qr {user.name}.png')


if __name__ == '__main__':
    name = input('Enter the name of the user : ')
    user = search_user(name=name)
    if user is None:
        issuer_name = input('Enter the issuer name : ')
        user = Person(name=name, secret=SECRET, issuer_name=issuer_name)
        save_user(user=user)
        get_qrcode(user)
        totp = pyotp.TOTP(user.secret)
    else:
        get_qrcode(user)    
        totp = pyotp.TOTP(user.secret)
    while True:
        print(totp.verify(input('Enter the Code : ')))