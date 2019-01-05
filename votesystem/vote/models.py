from django.db import models
from django.db.models import Sum

# Create your models here.
class Candidate(models.Model):
    name = models.CharField(max_length=50)
    area = models.CharField(max_length=50)

    def __str__(self):
        return '{}-{}'.format(self.name,self.area)

    

class Poll(models.Model):
    area = models.CharField(max_length=50)
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)

    def __str__(self):
        return '{}'.format(self.area)


class Vote(models.Model):
    can_for=models.ForeignKey(Candidate, on_delete=models.CASCADE, null=True)
    poll_for=models.ForeignKey(Poll, on_delete=models.CASCADE, null=True)
    vote_count=models.IntegerField(default=0)

    def __str__(self):
        return '{}-{}'.format(self.can_for.name,self.vote_count)

    def avg(self):
        result = Vote.objects.filter(poll_for__id=self.poll_for.id).aggregate(vote_sum = Sum('vote_count'))
        avg = self.vote_count/result['vote_sum']
        return '{0:.2f}'.format(avg)

class Noti(models.Model):
    message=models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.message)