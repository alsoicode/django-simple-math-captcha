from __future__ import absolute_import
from __future__ import unicode_literals

import mock

from django.core.exceptions import ValidationError
from django.test import TestCase

from simplemathcaptcha.widgets import MathCaptchaWidget
from simplemathcaptcha.fields import MathCaptchaField


class FieldTests(TestCase):

    def test_instantiation(self):
        f = MathCaptchaField()
        self.assertTrue(f.required)
        self.assertTrue(f.widget.is_required)
        self.assertEqual(len(f.fields), 2)

    @mock.patch('simplemathcaptcha.fields.MathCaptchaWidget')
    def test_instantiation_with_values(self, mocked):
        MathCaptchaField(start_int=5, end_int=10)
        mocked.assert_called_once_with(start_int=5, end_int=10)

    @mock.patch('simplemathcaptcha.fields.MathCaptchaWidget')
    def test_instantiation_with_widget(self, mocked):
        MathCaptchaField(widget=MathCaptchaWidget())
        self.assertEqual(mocked.call_count, 0)

    def test_instantiation_with_widget_and_values_is_error(self):
        with self.assertRaises(TypeError):
            MathCaptchaField(start_int=5, end_int=10,
                             widget=MathCaptchaWidget())

    def test_compress(self):
        f = MathCaptchaField()
        with mock.patch('simplemathcaptcha.fields.hash_answer') as mocked:
            mocked.return_value = 'hashed_answer'
            result = f.compress(['abc', 'hashed_answer'])
            self.assertIsNone(result)

    def test_compress_with_wrong_answer(self):
        f = MathCaptchaField()
        with mock.patch('simplemathcaptcha.fields.hash_answer') as mocked:
            mocked.return_value = 'bad_hashed_answer'
            with self.assertRaises(ValidationError):
                f.compress(['abc', 'hashed_answer'])

    def test_compress_with_nothing(self):
        f = MathCaptchaField()
        result = f.compress([])
        self.assertIsNone(result)
