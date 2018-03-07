from django.db import models

# Create your models here.
class Title(models.Model):
    title_text = models.CharField(max_length=200)
    title_date = models.DateTimeField('Date Published')

    def __str__(self):
        return self.title_text