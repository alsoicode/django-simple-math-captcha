from django.core.exceptions import ValidationError
from django import forms
from django.forms.fields import MultiValueField, IntegerField, CharField
from django.template.defaultfilters import mark_safe

from utils import hash_question, unhash_question, eval_answer, \
    get_operator, get_numbers


class MathCaptchaWidget(forms.MultiWidget):
    def __init__(self, attrs=None):
        self.attrs = attrs or {}
        widgets = (
            forms.TextInput(attrs={'size' : '5'}), #this is the answer input field
            forms.HiddenInput() #this is the hashed question field to compare to
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
        return u'%s%s' % (rendered_widgets[0], rendered_widgets[1])


class MathCaptchaField(MultiValueField):
    widget = MathCaptchaWidget

    def __init__(self, start_int=0, end_int=10, \
                 error_message='Please check your math and try again', \
                 *args, **kwargs):

        #set up error messages
        self.error_message = error_message
        errors = self.default_error_messages.copy()
        if 'error_messages' in kwargs:
            errors.update(kwargs['error_messages'])
        localize = kwargs.get('localize', False)

        #get integers for question
        x, y = get_numbers(start_int, end_int)

        #set up question
        operator = get_operator()
        question = '%i %s %i' % (x, operator, y)

        #make multiplication operator more human-readable
        operator_for_label = '&times;' if operator == '*' else operator

        #set label for field
        kwargs['label'] = mark_safe('What is %i %s %i' % (x, operator_for_label, y))

        #hash question and set initial value of form
        hashed_question = hash_question(question)
        kwargs['initial'] = '%s|%s' % ('', hashed_question)

        #set fields
        fields = (
            IntegerField(min_value=0, localize=localize),
            CharField(max_length=255)
        )
        super(MathCaptchaField, self).__init__(fields, *args, **kwargs)

    def compress(self, data_list):
        """Compress takes the place of clean with MultiValueFields"""
        if data_list:
            answer = data_list[0]
            #unhash and eval question. Compare to answer.
            unhashed_question = unhash_question(data_list[1])
            unhashed_answer = eval_answer(unhashed_question)
            if answer != unhashed_answer:
                raise ValidationError(self.error_message)
            return answer
        return None
