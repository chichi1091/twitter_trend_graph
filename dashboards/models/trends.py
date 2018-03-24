from django.db import models


class Trends(models.Model):
    target_date = models.DateField(auto_now_add=True)
    word = models.TextField()
    count = models.IntegerField(default=0)
