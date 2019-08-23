from django.core.exceptions import ValidationError
from django.test import TestCase

from .validators import nick_validator, string_only_letters_validator

class TestNickValidator(TestCase):

    def setUp(self):
        """
        Install necessery word for test.
        Three good (with numbers, letters and number, letters)
        Two bad (with special sign)
        """
        self.word_only_letters = 'tester'
        self.word_only_numbers = '1212121'
        self.word_with_letters_numbers = 'tester1996'
        self.word_with_special_sign = '@!tester123'
        
    def test_with_word_which_have_only_letter(self):
        """
        Test validator with word which have only letters.
        The test consists of checking the correctness of the nickname,
        if word have only letters nick is correct
        """
        self.assertEqual(nick_validator(self.word_only_letters), None)

    def test_with_word_which_have_only_numbers(self):
        """
        Test validator with word which have only numbers.
        The test consists of checking the correctness of the nickname,
        if word have only numbers nick is correct
        """
        self.assertEqual(nick_validator(self.word_only_numbers), None)

    def test_with_word_which_have_numbers_and_letters(self):
        """
        Test validator with word which have numbers and letters.
        The test consists of checking the correctness of the nickname,
        if word have numbers and letters nick is correct
        """
        self.assertEqual(nick_validator(self.word_with_letters_numbers), None)

    def test_with_word_which_have_numbers_letters_and_special_signs(self):
        """
        Test validator with word which have numbers, letters and special signs.
        The test consists of checking the correctness of the nickname,
        if word have numbers letters and special signs nick is discorrect
        """
        with self.assertRaises(ValidationError) as error:
            nick_validator(self.word_with_special_sign)

class TestStringOnlyLetterValidator(TestCase):

    def setUp(self):
        """
        Install necessery word for test.
        Three bad (with numbers, letters and number, special signs)
        One good (with letters)
        """
        self.word_only_letters = 'tester'
        self.word_only_numbers = '1212121'
        self.word_with_letters_numbers = 'tester1996'
        self.word_with_special_sign = '@!tester123'

    def test_with_word_which_have_only_letter(self):
        """
        Test validator with word which have only letters.
        The test consists of checking the correctness of the string,
        if word have only letters string is correct
        """
        self.assertEqual(string_only_letters_validator(self.word_only_letters), None)

    def test_with_word_which_have_only_numbers(self):
        """
        Test validator with word which have only numbers.
        The test consists of checking the correctness of the string,
        if word have only numbers string is discorrect
        """
        with self.assertRaises(ValidationError) as error:
            string_only_letters_validator(self.word_only_numbers)

    def test_with_word_which_have_numbers_and_letters(self):
        """
        Test validator with word which have numbers and letters.
        The test consists of checking the correctness of the string,
        if word have numbers and letters string is discorrect
        """
        with self.assertRaises(ValidationError) as error:
            string_only_letters_validator(self.word_with_letters_numbers)

    def test_with_word_which_have_numbers_letters_and_special_signs(self):
        """
        Test validator with word which have numbers, letters and special signs.
        The test consists of checking the correctness of the string,
        if word have numbers letters and special signs string is discorrect
        """
        with self.assertRaises(ValidationError) as error:
            string_only_letters_validator(self.word_with_special_sign)



