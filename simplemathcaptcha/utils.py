from binascii import hexlify
from random import randint, choice
from hashlib import sha1

from django.conf import settings

from .constants import OPERATORS


def hash_answer(value):
    answer = str(value)
    return sha1(settings.SECRET_KEY + answer).hexdigest() + hexlify(answer)


def get_operator():
    return choice(OPERATORS)


def get_numbers(start_int, end_int):
    if start_int < 0 or end_int < 0:
        raise Warning(u'MathCaptchaField requires positive integers '
                      u'for start_int and end_int.')
    try:
        x = randint(start_int, end_int)
        y = randint(start_int, end_int)
    except ValueError:
        x = randint(1, 10)
        y = randint(1, 10)

    #avoid negatives
    if y > x:
        x, y = y, x
    return x, y
