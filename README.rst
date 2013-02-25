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
You can do any of the following to install `django-simple-math-captcha`

* Run ``pip install django-simple-math-captcha``.

* Download or "git clone" the package and run ``setup.py``.

* Download or "git clone" the package and put the ``simplemathcaptcha``
  directory on your PYTHONPATH.

Usage
=============
Forms
----------------------
To add the captcha field to your form:

from django import forms
from simplemathcaptcha.fields import MathCaptchaField
    
class MyForm(forms.Form):
    some_text_field = models.CharField(max_length=50)
    captcha = MathCaptchaField()

Optionally, you can pass in the following arguments to the field to configure it.

`start_int` - The number at which the field should begin its range of random numbers.
              This value will be used passed into the creation of an
              `simplemathcaptcha.widgets.MathCaptchaWidget` for this field.
                  The default value is: 1.

`end_int` - The number at which the field should end its range of random numbers.
            This value will be used passed into the creation of an
            `simplemathcaptcha.widgets.MathCaptchaWidget` for this field.
                The default value is: 10.

`error_messages` - A dictionary of error messages.  The keys you can use are `invalid`
                   and `invalid_number`.  `invalid` is the message to display when the
                   provided answer is incorrect and the default value is: 'Check your 
                   math and try again.'  `invalid_number` is the message to display
                   when the entry is not a whole number and the default value is: 
                   'Enter a whole number.'

`question_class` - A css class to use for the span containing the displayed question.
                       The default value is: 'captcha-question'

`widget` - The widget instance to use, instead of the
           default `simplemathcaptcha.widgets.MathCaptchaWidget`.  When provided, it
           must be an instatiated widget, not a widget class.  Additionally, when
           specifying `widget`, you must not specify `start_int` or `end_int`


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
- Question asked changes with every render
- Uses SHA1 hashing of answer with your SECRET_KEY
- Unit tests are provided in the source

Requirements
=============
Python 2.6+
Django 1.4+

License
=============
The django-simple-math-captcha app is released under the Apache Public License v2.
