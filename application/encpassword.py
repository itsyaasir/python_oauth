from passlib.context import CryptContext

"""This module is used for import the passlib mainly for authentication"""

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)


def encrypt(password):
    return pwd_context.hash(password)


def decrypt(password, hash):
    return pwd_context.verify(password, hash)
#
# print(encrypt("test"))
# print(decrypt("test" , encrypt("test")))
