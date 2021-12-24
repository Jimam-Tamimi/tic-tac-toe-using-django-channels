from django.db import models

# Create your models here.


class Game(models.Model):
    creator = models.CharField(max_length=100, blank=True, null=True)
    opponent = models.CharField(max_length=100, blank=True, null=True)
    room_code = models.CharField(max_length=30, blank=False, null=False)

    def __str__(self):
        return self.room_code