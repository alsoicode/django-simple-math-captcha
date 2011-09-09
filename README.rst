=============
django-simple-math-captcha
=============

What is it?
=============
A multi-value-field that presents a human answerable question,
with no settings.py configuration necessary, but instead can be
configured with arguments to the field constructor.

Installation
=============
1. Run ``setup.py`` or add ``simplemathcaptcha`` to your PYTHONPATH.
2. Add ``simplemathcaptcha`` to your INSTALLED_APPS.
3. Have a look at the included sample_project to see a working example and to run unit tests.

Usage
=============
Forms
----------------------
To add the captcha field to your form:

`from django import forms
from simplemathcaptcha.fields import MathCaptchaField

class MyForm(forms.Form):
    some_text_field = models.CharField(max_length=50)
    captcha = MathCaptchaField(required=True)`

You must manually set the field to required, as MultiValueFields make all
fields optional when the field in initialized. Optionally, you can pass in 3
arguments to the field to configure it.

`start_int` - The number at which the field should begin its range of random numbers.
                  The default value is: 10.

`end int` - The number at which the field should end its range of random numbers
                The default value is: 10.

`error_message` - The message to display when the provided answer is incorrect.
                           The default value is: 'Check your math and try again.' 


Rationale
=============
Other math captcha fields can present questions that require decimal answers,
answers that could be negative values and that require settings.py configuration.
This project aims to provide a single field with minimal or no configuration
necessary and reduce or prevent spam form submissions.

Status
=============
django-simple-math-captcha is currently used in production.

Feautures
=============
- Simple addition, subtraction or multiplication question for captcha
- No configuration necessary
- Uses SHA1 hashing of question
- Unit tests are provided as part of included sample_app in source

Requirements
=============
Django 1.x+

License
=============
The admin-sortable app is released 
under the Apache Public License v2.
