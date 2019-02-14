from __future__ import absolute_import
from __future__ import unicode_literals

import mock

from django import forms
from django.utils import six
from django.test import TestCase

from simplemathcaptcha.fields import MathCaptchaField
from simplemathcaptcha import utils


class FormTests(TestCase):

    @mock.patch('simplemathcaptcha.widgets.get_operator')
    @mock.patch('simplemathcaptcha.widgets.hash_answer')
    @mock.patch('simplemathcaptcha.utils.randint')
    def test_form(self, mock_randint, mock_hash_answer, mock_get_operator):

        ops = ['+', '-']
        ints = [1, 3, 1, 3]
        mock_randint.side_effect = lambda x, y: ints.pop(0)
        mock_hash_answer.side_effect = lambda x: "answer=%s" % x
        mock_get_operator.side_effect = lambda: ops.pop(0)

        class F(forms.Form):
            captcha = MathCaptchaField()

        f = F()
        result1 = six.text_type(f)
        result2 = six.text_type(f)
        self.assertHTMLEqual(result1, """
            <tr><th><label for="id_captcha_0">Captcha:</label></th><td>
                <span class="captcha-question">What is 1 + 3?</span>
                <input id="id_captcha_0" required name="captcha_0"
                       size="5" type="text" />
                <input id="id_captcha_1" required name="captcha_1"
                       type="hidden" value="answer=4" />
            </td></tr>""")

        self.assertHTMLEqual(result2, """
            <tr><th><label for="id_captcha_0">Captcha:</label></th><td>
                <span class="captcha-question">What is 3 - 1?</span>
                <input id="id_captcha_0" required name="captcha_0"
                       size="5" type="text" />
                <input id="id_captcha_1" required name="captcha_1"
                       type="hidden" value="answer=2" />
            </td></tr>""")

    def test_form_validation(self):
        class F(forms.Form):
            captcha = MathCaptchaField()

        hashed_answer = utils.hash_answer(5)

        f = F({'captcha_0': 5, 'captcha_1': hashed_answer})
        self.assertTrue(f.is_valid())

        f = F({'captcha_0': 4, 'captcha_1': hashed_answer})
        self.assertFalse(f.is_valid())
