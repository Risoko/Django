from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def nick_validator(value):
    """
    Validator nick, checks if all characters are letters and numbers.
    If not throws an exception.
    """
    for element in value:
        if not (element.isdigit() or element.isalpha()):
            raise ValidationError(
                message=_("Nick: %(value)s must be only letters and digits."),
                params=dict(value=value)
            )

def string_only_letters_validator(value):
    """
    Validator string, checks if all characters are letters.
    If not throws an exception.
    """
    for element in value:
        if not element.isalpha():
            raise ValidationError(
                message=_("String: %(value)s must be only digits"),
                params=dict(value=value)
            )



