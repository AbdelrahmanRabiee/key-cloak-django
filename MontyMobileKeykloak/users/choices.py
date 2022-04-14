from model_utils import Choices
from django.utils.translation import gettext_lazy as _

ROLE = Choices(
    ('normal_user', _('Normal User Role')),
    ('admin', _('Admin User Role')),
)