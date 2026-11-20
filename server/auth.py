import hashlib
import hmac
import os
import re

# PBKDF2 settings. More iterations = slower for an attacker to guess passwords from a stolen hash.
HASH_ALGORITHM = 'sha256'
ITERATIONS = 200_000
SALT_SIZE = 16  # bytes

USERNAME_PATTERN = re.compile(r'[A-Za-z0-9_]{3,20}')
MIN_PASSWORD_LENGTH = 8
MAX_PASSWORD_LENGTH = 128


def new_salt():
    # Random salt, different for every user, so two users with the same password get different hashes
    return os.urandom(SALT_SIZE)


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(HASH_ALGORITHM, password.encode('utf-8'), salt, ITERATIONS)


def verify_password(password, salt_hex, stored_hash_hex):
    # Hash the login attempt with the user's stored salt and compare it to the stored hash.
    # compare_digest takes the same time no matter where the bytes differ (prevents timing attacks).
    attempt = hash_password(password, bytes.fromhex(salt_hex))
    return hmac.compare_digest(attempt, bytes.fromhex(stored_hash_hex))


def is_valid_username(username):
    # fullmatch = the WHOLE string must match (3-20 letters, digits or underscores)
    return USERNAME_PATTERN.fullmatch(username) is not None


def is_valid_password(password):
    return MIN_PASSWORD_LENGTH <= len(password) <= MAX_PASSWORD_LENGTH
