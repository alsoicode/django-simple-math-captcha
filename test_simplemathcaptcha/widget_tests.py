from __future__ import absolute_import
from __future__ import unicode_literals

import mock

from django.utils import six
from django.test import TestCase

from simplemathcaptcha.widgets import MathCaptchaWidget


class WidgetTests(TestCase):

    # init
    def test_instantiation(self):
        w = MathCaptchaWidget(1, 10)
        self.assertEqual(len(w.widgets), 2)
        self.assertEqual(w.start_int, 1)
        self.assertEqual(w.end_int, 10)
        self.assertEqual(six.text_type(w.question_tmpl),
                         'What is %(num1)i %(operator)s %(num2)i? ')
        self.assertEqual(w.question_class, 'captcha-question')

    def test_default_question_tmpl(self):
        w = MathCaptchaWidget(question_tmpl='foo')
        self.assertEqual(w.question_tmpl, 'foo')

    def test_default_question_class(self):
        w = MathCaptchaWidget(question_class='foo')
        self.assertEqual(w.question_class, 'foo')

    def test_negative_start_int_raises(self):
        with self.assertRaises(Warning):
            MathCaptchaWidget(-1, 10)

    def test_negative_end_int_raises(self):
        with self.assertRaises(Warning):
            MathCaptchaWidget(1, -10)

    def test_end_int_less_than_start_int_raises(self):
        with self.assertRaises(Warning):
            MathCaptchaWidget(10, 1)

    # decompress tests
    def test_decompress_always_returns_none(self):
        w = MathCaptchaWidget()
        expected = [None, None]
        self.assertEqual(w.decompress(None), expected)
        self.assertEqual(w.decompress(''), expected)
        self.assertEqual(w.decompress('something'), expected)

    # render tests
    def test_render(self):
        w = MathCaptchaWidget()
        with mock.patch.object(w, 'generate_captcha') as mock_generate_captcha:
            mock_generate_captcha.return_value = 'hashed_answer'
            w.question_html = 'question_html'
            result = w.render('foo', None)
            self.assertHTMLEqual(result, """
            <span class="captcha-question">question_html</span>
            <input type="text" name="foo_0" size="5" />
            <input type="hidden" name="foo_1" value="hashed_answer"/>""")

    def test_render_is_different_each_time_called(self):
        w = MathCaptchaWidget()
        result1 = w.render('foo', None)
        result2 = w.render('foo', None)
        self.assertHTMLNotEqual(result1, result2)

    # generate captcha tests
    @mock.patch('simplemathcaptcha.widgets.get_operator')
    @mock.patch('simplemathcaptcha.widgets.get_numbers')
    @mock.patch('simplemathcaptcha.widgets.hash_answer')
    def test_generate_captcha(self, mock_hash_answer, mock_get_numbers,
                              mock_get_operator):
        mock_hash_answer.side_effect = lambda x: x
        mock_get_numbers.return_value = (1, 3)
        mock_get_operator.return_value = '+'
        w = MathCaptchaWidget()
        result = w.generate_captcha()
        self.assertEqual(result, 4)
        self.assertEqual(mock_hash_answer.call_count, 1)
        self.assertEqual(mock_get_numbers.call_count, 1)
        self.assertEqual(mock_get_operator.call_count, 1)
        self.assertHTMLEqual(w.question_html, "What is 1 + 3?")

    # set question tests
    def test_set_question(self):
        w = MathCaptchaWidget()
        w.set_question(2, 4, 'foo')
        self.assertHTMLEqual(w.question_html, "What is 2 foo 4?")

    def test_set_question_converts_multiplication_operator_to_entity(self):
        w = MathCaptchaWidget()
        w.set_question(2, 4, '*')
        self.assertHTMLEqual(w.question_html, "What is 2 &times; 4?")
