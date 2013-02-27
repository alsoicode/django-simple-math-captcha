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
    author_email='brandon@iambrandontaylor.com',
    url='http://iambrandontaylor.com/',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    classifiers=['Development Status :: 4 - Beta',
                   'Environment :: Web Environment',
                   'Framework :: Django',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Utilities'],
)
