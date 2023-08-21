from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class DjDT_PermissionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'djdt_permissions'
    verbose_name = _('Django Debug Toolbar Permissions Panel')
