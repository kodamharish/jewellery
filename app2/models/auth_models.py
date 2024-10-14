from django.db import models
from django.contrib.auth.hashers import make_password
#Create your models here.
class User(models.Model):
    username = models.CharField(max_length=100,primary_key=True)
    password = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    #last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.IntegerField()


    def save(self, *args, **kwargs):
        # Hash the password before saving
        if self.password:
            self.password = make_password(self.password)
        super().save(*args, **kwargs)