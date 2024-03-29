from django.db import models

# Create your models here.

class userInformation(models.Model):
    userId = models.CharField(max_length=150)
    userName = models.CharField(max_length=200)
    fullName = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=200, null=True)

    def __str__(self):
        return (self.userName)


class messageInformation(models.Model):
    author = models.CharField(max_length=200)
    textMessage = models.TextField()
    timeStamp = models.CharField(max_length=200)
    channel = models.CharField(max_length=100)

    def __str__(self):
        return (self.textMessage)

class upload(models.Model):
    title = models.CharField(max_length=100)
    fileId = models.CharField(max_length=50)
    file = models.CharField(max_length=200)

