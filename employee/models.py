from django.db import models

ST = (
    (1, 'Active'),
    (0, 'In-Active'),
)
class Bank(models.Model):
    name = models.CharField(max_length=200, unique=True)
    status = models.IntegerField(choices=ST,blank=True)

    def __str__(self):
        return self.name