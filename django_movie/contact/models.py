from django.db import models
from django.utils.translation import gettext_lazy as _

class Contact(models.Model):
    '''Подписка по email'''
    email = models.EmailField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "contacts"
        verbose_name = _("Контакт")
        verbose_name_plural = _("Контакты")
