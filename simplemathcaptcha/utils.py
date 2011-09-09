from binascii import hexlify, unhexlify
from random import randint, choice

from django.conf import settings
from django.utils.hashcompat import sha_constructor

from constants import OPERATORS


def hash_question(question):
    return sha_constructor(settings.SECRET_KEY \
                                    + question).hexdigest() + hexlify(question)

def unhash_question(question):
    return unhexlify(question[40:])

def eval_answer(unhashed_question):
    return eval(unhashed_question)

def get_operator():
    return choice(OPERATORS)

def get_numbers(start_int, end_int):
    if start_int < 0 or end_int < 0:
        raise Warning(u'MathCaptchaField requires positive integers for start_int and end_int.')
    try:
        x = randint(start_int, end_int)
        y = randint(start_int, end_int)
    except ValueError:
        x = randint(10, 10)
        y = randint(10, 10)

    #avoid negatives
    if y > x:
        x, y = y, x
    return x, y
