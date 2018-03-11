from django.db import models

# Create your models here.
class Title(models.Model):
    title_text = models.CharField(max_length=200)
    title_date = models.DateTimeField('Date Published')

    def __str__(self):
        return self.title_text

class Meeting(models.Model):
    create_date=models.DateTimeField('Date Published',auto_now_add=True)
    start_date=models.DateTimeField('Date start')
    end_date=models.DateTimeField('Date end')
    meeting_user=models.CharField(max_length=200)
    meeting_content=models.CharField(max_length=300)

    def __str__(self):
        return self.meeting_content

    class Meta:
        ordering=['start_date']