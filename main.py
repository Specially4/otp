import time
import pyotp
import qrcode
from PIL import Image

from constants import SECRET
from registry import get_uri, get_qrcode
from db.db import save_user, Person


totp = pyotp.TOTP(SECRET)

while True:
    print(totp.verify(input('Enter the Code : ')))
    