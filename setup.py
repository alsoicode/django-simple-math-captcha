from setuptools import setup, find_packages

try:
    README = open('README.rst').read()
except:
    README = None

setup(
    name='django-simple-math-captcha',
    version=__import__('simplemathcaptcha').__version__,
    description='An easy-to-use math field/widget captcha for Django forms.',
    long_description=README,
    author='Brandon Taylor',
    author_email='alsoicode@gmail.com',
    url='https://alsoicode.github.io/',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=['Development Status :: 5 - Production/Stable',
               'Environment :: Web Environment',
               'Framework :: Django',
               'Intended Audience :: Developers',
               'License :: OSI Approved :: Apache Software License',
               'Operating System :: OS Independent',
               'Programming Language :: Python',
               'Programming Language :: Python :: 2.7',
               'Programming Language :: Python :: 3',
               'Programming Language :: Python :: Implementation :: CPython',
               'Topic :: Utilities'],
)
