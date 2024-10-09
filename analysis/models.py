from django.db import models

class DiscordMessage(models.Model):
    author = models.CharField(max_length=100)
    content = models.TextField()
    channel = models.CharField(max_length=100)
    sentiment = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.sentiment}"
