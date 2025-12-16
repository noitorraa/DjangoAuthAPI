from django.db import models
from django.utils.translation import gettext_lazy as _


class MockObject(models.Model):
    """Модель для тестовых объектов"""
    
    name = models.CharField(_("name"), max_length=100)
    description = models.TextField(_("description"), blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        verbose_name = _("mock object")
        verbose_name_plural = _("mock objects")

    def __str__(self):
        return self.name
