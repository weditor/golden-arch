from django.db import models
from user.models import HxUser

# Create your models here.


class Conference(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default="")
    creator = models.ForeignKey(HxUser, on_delete=models.CASCADE)
    holding_time = models.DateTimeField()

    def __str__(self):
        return self.name


class ConferenceTopic(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, default="")
    creator = models.ForeignKey(HxUser, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)

    claim_user = models.ForeignKey(
        HxUser,
        related_name="claim_conference_topics",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
    )
    claim_time = models.DateTimeField(blank=True, null=True)
    like_user = models.ManyToManyField(HxUser, related_name="like_conference_topics")
    conference = models.ForeignKey(
        Conference, blank=True, null=True, on_delete=models.CASCADE
    )

    def __str__(self):
        return self.name
