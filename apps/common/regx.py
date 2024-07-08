import re
from django.core.exceptions import ValidationError


def validate_uzbekistan_phone_number(value):
    uzbekistan_phone_regex = r'^\+998[- ]?\d{2}[- ]?\d{3}[- ]?\d{4}$|^0\d{2}[- ]?\d{3}[- ]?\d{4}$'
    if not re.match(uzbekistan_phone_regex, value):
        raise ValidationError(f'{value} is not a valid Uzbekistan phone number.')