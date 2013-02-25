from __future__ import absolute_import
from __future__ import unicode_literals

from random import randint, choice
from hashlib import sha1

from django.conf import settings
from django.utils import six

MULTIPLY = '*'
ADD = '+'
SUBTRACT = '-'
CALCULATIONS = {
    MULTIPLY: lambda a, b: a * b,
    ADD: lambda a, b: a + b,
    SUBTRACT: lambda a, b: a - b,
}
OPERATORS = tuple(CALCULATIONS)


def hash_answer(value):
    answer = six.text_type(value)
    return sha1(settings.SECRET_KEY + answer).hexdigest()


def get_operator():
    return choice(OPERATORS)


def get_numbers(start_int, end_int, operator):
    x = randint(start_int, end_int)
    y = randint(start_int, end_int)

    #avoid negative results for subtraction
    if y > x and operator == SUBTRACT:
        x, y = y, x

    return x, y


def calculate(x, y, operator):
    func = CALCULATIONS[operator]
    total = func(x, y)
    return total

