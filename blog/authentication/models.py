from django.conf import settings
from django.core.validators import MinLengthValidator
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from .validators import nick_validator, string_only_letters_validator

class User(AbstractUser):
    nick = models.CharField(
        _('nick'),
        max_length=50,
        unique=True,
        help_text=_('Required. 50 characters or fewer. Letters, digits.'),
        validators=[nick_validator, MinLengthValidator(5)],
        error_messages={
            'unique': _("A user with that nick already exists."),
        }
    )
    first_name = models.CharField(
        _('first name'),
        max_length=30,
        validators=[string_only_letters_validator],
        help_text=_('Required. 30 characters or fewer. Letters.')
    )
    last_name = models.CharField(
        _('last name'), 
        max_length=150,
        validators=[string_only_letters_validator],
        help_text=_('Required. 150 characters or fewer. Letters.')
    )
    email = models.EmailField(
        _('email address'), 
        unique=True,
        error_messages={
            'unique': _("A user with that email address already exists."),
        }
    )
    birth_date = models.DateField(
        _('birth date'),
        help_text=_('Required format YEAR-MONTH-DAY. Example 1996-12-03')

    )
    number_article = models.PositiveIntegerField(
        _('number of article'),
        default=0
    )

    def __str__(self):
        return self.nick
