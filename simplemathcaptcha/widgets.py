from __future__ import absolute_import
from __future__ import unicode_literals

from django import forms
from django.template.defaultfilters import mark_safe
from django.utils.translation import ugettext_lazy as _

from .utils import hash_answer, get_operator, get_numbers, calculate


class MathCaptchaWidget(forms.MultiWidget):
    template_name = "simplemathcaptcha/captcha.html"

    def __init__(self, start_int=1, end_int=10, question_tmpl=None,
                 question_class=None, attrs=None):
        self.start_int, self.end_int = self.verify_numbers(start_int, end_int)
        self.question_class = question_class or 'captcha-question'
        self.question_tmpl = (
            question_tmpl or _('What is %(num1)i %(operator)s %(num2)i? '))
        self.question_html = None
        widget_attrs = {'size': '5'}
        widget_attrs.update(attrs or {})
        widgets = (
            # this is the answer input field
            forms.TextInput(attrs=widget_attrs),

            # this is the hashed answer field to compare to
            forms.HiddenInput()
        )
        super(MathCaptchaWidget, self).__init__(widgets, attrs)

    def get_context(self, *args, **kwargs):
        context = super(MathCaptchaWidget, self).get_context(*args, **kwargs)
        context['question_class'] = self.question_class
        context['question_html'] = self.question_html
        return context

    def decompress(self, value):
        return [None, None]

    def render(self, name, value, attrs=None, renderer=None):
        # hash answer and set as the hidden value of form
        hashed_answer = self.generate_captcha()
        value = ['', hashed_answer]

        return super(MathCaptchaWidget, self).render(name, value, attrs=attrs, renderer=renderer)

    def generate_captcha(self):
        # get operator for calculation
        operator = get_operator()

        # get integers for calculation
        x, y = get_numbers(self.start_int, self.end_int, operator)

        # set question to display in output
        self.set_question(x, y, operator)

        # preform the calculation
        total = calculate(x, y, operator)

        return hash_answer(total)

    def set_question(self, x, y, operator):
        # make multiplication operator more human-readable
        operator_for_label = '&times;' if operator == '*' else operator
        question = self.question_tmpl % {
            'num1': x,
            'operator': operator_for_label,
            'num2': y
        }

        self.question_html = mark_safe(question)

    def verify_numbers(self, start_int, end_int):
        start_int, end_int = int(start_int), int(end_int)
        if start_int < 0 or end_int < 0:
            raise Warning('MathCaptchaWidget requires positive integers '
                          'for start_int and end_int.')
        elif end_int < start_int:
            raise Warning('MathCaptchaWidget requires end_int be greater '
                          'than start_int.')
        return start_int, end_int
