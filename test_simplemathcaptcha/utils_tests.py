from __future__ import absolute_import
from __future__ import unicode_literals

import mock

from django.utils import six
from django.test import TestCase

from simplemathcaptcha import utils


class UtilsTests(TestCase):

    def test_get_numbers(self):
        x, y = utils.get_numbers(1, 1, '+')
        self.assertEqual((x, y), (1, 1))

    @mock.patch('simplemathcaptcha.utils.randint')
    def test_get_numbers_changes_order(self, mocked):
        vals = [1, 5]
        mocked.side_effect = lambda a, b: vals.pop(0)
        x, y = utils.get_numbers(1, 5, '-')
        self.assertEqual((x, y), (5, 1))

    @mock.patch('simplemathcaptcha.utils.randint')
    def test_get_numbers_does_not_change_order(self, mocked):
        vals = [1, 5, 1, 5]
        mocked.side_effect = lambda a, b: vals.pop(0)
        x, y = utils.get_numbers(1, 5, '+')
        self.assertEqual((x, y), (1, 5))
        x, y = utils.get_numbers(1, 5, '*')
        self.assertEqual((x, y), (1, 5))

    def test_calculate_adding(self):
        result = utils.calculate(1, 1, '+')
        self.assertEqual(result, 2)

    def test_calculate_subtracting(self):
        result = utils.calculate(1, 1, '-')
        self.assertEqual(result, 0)

    def test_calculate_multiplying(self):
        result = utils.calculate(1, 1, '*')
        self.assertEqual(result, 1)

    def test_calculate_raises_on_unknown_op(self):
        with self.assertRaises(KeyError):
            utils.calculate(1, 1, '/')

    def test_hash_answer_is_string(self):
        result = utils.hash_answer(1)
        self.assertIsInstance(result, six.string_types)

    def test_hash_answer_is_repeatable(self):
        result1 = utils.hash_answer(1)
        result2 = utils.hash_answer(1)
        self.assertEqual(result1, result2)

    def test_hash_answer_returns_hexdigest(self):
        result = utils.hash_answer(1)
        self.assertEqual(len(result), 40)
