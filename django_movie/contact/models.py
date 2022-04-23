from django.db import models


class Contact(models.Model):
    '''Подписка по email'''
    email = models.EmailField()
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = "contacts"
        verbose_name = "Контакт"
        verbose_name_plural = "Контакты"
