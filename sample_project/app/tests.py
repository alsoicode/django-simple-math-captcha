from django.test import TestCase
from django.test.client import Client, RequestFactory

from app.forms import SampleForm
from simplemathcaptcha.utils import hash_question, unhash_question, \
    eval_answer, get_operator, get_numbers


class MathCaptchaTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_hash_question(self):
        hashed_question = hash_question('3 + 5')
        self.assertEqual(hashed_question,
                         'e5177d021897d83043b0e091d0c96a2283cd4ca233202b2035',
                         'Question was not properly hashed')

    def test_unhash_question(self):
        x, y = get_numbers(start_int=5, end_int=5)
        operator = get_operator()
        question = '%i %s %i' % (x, operator, y)
        hashed_question = hash_question(question)
        unhashed_question = unhash_question(hashed_question)
        self.assertEqual(question, unhashed_question,
                         'Question was not properly un-hashed')

    def test_get_numbers_returns_integers_that_result_in_positive_answer(self):
        x, y = get_numbers(start_int=5, end_int=5)
        self.assertGreaterEqual(x, y, u'Get numbers returned integers that '
                                'would result in a negative answer.')

    def test_eval_answer(self):
        #create question that we can provide an answer for and hash it
        hashed_question = hash_question('3 + 5')

        #unhash the question and compare it to the answer we provide
        unhashed_question = unhash_question(hashed_question)
        evaluated_answer = eval_answer(unhashed_question)

        our_answer = 8
        self.assertEqual(our_answer, evaluated_answer, u'The answers did not match. '
            'The evaled answer was %i and we said it was %i' % (evaluated_answer, our_answer))
