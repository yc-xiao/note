from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=200)
    info = models.TextField()

    def to_json(self):
        return {'name': self.name, 'password': self.password, 'info': self.info}

    class Meta:
        verbose_name = '用户表'