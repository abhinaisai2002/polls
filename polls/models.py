from django.db import models
from datetime import datetime
# Create your models here.
from django.contrib.auth.models import User
from django.utils import timezone


class Poll(models.Model):
    title = models.CharField(max_length=50)
    date = models.DateTimeField(default=datetime.now)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return self.title


class PollsOptions(models.Model):
    pollOption = models.CharField(max_length=30)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    pollOptionVotes = models.IntegerField(default=0)

    def __str__(self) :
        return self.poll.title + ' ' +self.pollOption

class CommentBy(models.Model):
    poll = models.ForeignKey(Poll,on_delete=models.CASCADE)
    comment = models.TextField(null=True)
    comment_by = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)

class VotedBy(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    polled_by = models.ForeignKey(User,on_delete=models.CASCADE)
    polledOpt = models.ForeignKey(PollsOptions,on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.now)
