from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Theme(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Poll(models.Model):
    question = models.CharField(max_length=100)
    text = models.CharField(max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(User, related_name='polls', on_delete=models.CASCADE)
    theme = models.ForeignKey(Theme, related_name='polls', on_delete=models.CASCADE)

    @property
    def getResults(self):
        totalVotes = self.votes.all().count()

        if totalVotes > 0:
            numberYes = self.votes.filter(option=True).count()
            numberNo = self.votes.filter(option=False).count()

            percentageYes = 100 * numberYes / totalVotes
            percentageNo = 100 * numberNo / totalVotes

            return "Rezultate: {}% DA, {}% NU (Total: {} voturi)".format(percentageYes, percentageNo, totalVotes)

        else:
            return "Încă nu a votat nimeni!"

class Vote(models.Model):
    option = models.BooleanField()
    poll = models.ForeignKey(Poll, related_name='votes', on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='votes', on_delete=models.CASCADE)


