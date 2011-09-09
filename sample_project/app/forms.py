from django import forms

from simplemathcaptcha.fields import MathCaptchaField


class SampleForm(forms.Form):
    message = forms.CharField(max_length=255)
    captcha = MathCaptchaField(required=True)
