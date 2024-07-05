import os
import pyotp
import time

SALT = os.urandom(32)
SECRET = pyotp.random_base32()