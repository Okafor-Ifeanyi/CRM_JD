from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    pass

class Lead(models.Model):
    first_name = models.CharField(max_length=60)
    last_name = models.CharField(max_length=60)
    age = models.IntegerField(default=18)
    agent = models.ForeignKey("Agent", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

    # source_choices = (
    #     ('YT', 'YouTube'),
    #     ('Google', 'Google'),
    #     ('Newsletter', "Newsletter")
    # )

    # phoned = models.BooleanField(default=False)
    # source = models.CharField(choices=source_choices, max_length=20)

    # profile_picture = models.ImageField(blank=True, null=True)
