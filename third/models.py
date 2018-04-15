from django.db import models

#用户
class User(models.Model):
    email = models.CharField(max_length=254,primary_key=True)
    password = models.CharField(max_length=128)
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

#日志主档
class Logacn(models.Model):
    title=models.CharField(max_length=200)
    pub_date=models.DateTimeField()

    def __str__(self):
        return self.title

#日志明细档
class Logtxn(models.Model):
    logacn=models.ForeignKey(Logacn)
    content=models.CharField(max_length=400)

    def __str__(self):
        return self.content


class Test(models.Model):
    title=models.CharField(max_length=200)
    content=models.TextField(max_length=500)
    pub_date=models.DateTimeField()

    def __str__(self):
        return self.title