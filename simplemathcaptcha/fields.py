from django.core.exceptions import ValidationError
from django import forms
from django.forms.fields import MultiValueField, IntegerField, CharField
from django.template.defaultfilters import mark_safe

from .utils import hash_answer, get_operator, get_numbers


class MathCaptchaWidget(forms.MultiWidget):
    def __init__(self, start_int=0, end_int=10, attrs=None):
        self.start_int = start_int
        self.end_int = end_int
        self.attrs = attrs or {'size': '5'}
        widgets = (
            # this is the answer input field
            forms.TextInput(attrs=attrs),

            # this is the hashed answer field to compare to
            forms.HiddenInput()
        )
        super(MathCaptchaWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            """
            Split the initial value set by the field that implements
            this field and return the double. These values get bound
            to the fields.
            """
            question, hashed_question = value.split('|')
            return [question, hashed_question]
        return [None, None]

    def format_output(self, rendered_widgets):
        output = u'%s%s' % (rendered_widgets[0], rendered_widgets[1])
        output = u'<span>%s</span>%s' % (self.question, output)
        return output
    
    def render(self, name, value, attrs=None):
        # get integers for calculation
        x, y = get_numbers(self.start_int, self.end_int)
        
        # set up question and answer
        operator = get_operator()
        calc = {
            '*': lambda a, b: a * b,
            '+': lambda a, b: a + b,
            '-': lambda a, b: a - b,
        }
        total = calc[operator](x, y)
        
        # make multiplication operator more human-readable
        operator_for_label = '&times;' if operator == '*' else operator
        
        # set question to display in output
        self.question = mark_safe(
            'What is %i %s %i?' % (x, operator_for_label, y))
        
        # hash answer and set as the hidden value of form
        value = ['', hash_answer(total)]
        
        return super(MathCaptchaWidget, self).render(name, value, attrs=attrs)


class MathCaptchaField(MultiValueField):
    widget = MathCaptchaWidget

    def __init__(self, start_int=0, end_int=10, \
                 error_message='Please check your math and try again', \
                 *args, **kwargs):

        # set up error messages
        self.error_message = error_message
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', False)
        kwargs['widget'] = MathCaptchaWidget(start_int, end_int)

        # set fields
        fields = (
            IntegerField(min_value=0, localize=localize),
            CharField(max_length=255)
        )
        super(MathCaptchaField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        """Compress takes the place of clean with MultiValueFields"""
        if data_list:
            answer = data_list[0]
            real_hashed_answer = data_list[1]
            hashed_answer = hash_answer(answer)
            if hashed_answer != real_hashed_answer:
                raise ValidationError(self.error_message)
        return None
