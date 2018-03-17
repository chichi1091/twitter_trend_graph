from django.db import models


class Tweets(models.Model):
    text = models.TextField()
    tweet_date = models.DateTimeField(auto_now_add=True)
