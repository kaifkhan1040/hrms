from django.db import models
from django.conf import settings
import datetime

from attendee.models import Employee
from hierarchy.models import WaiverType, Branch

IO = (
    (1, 'In'),
    (2, 'Out'),
    (3, 'Other'),
)
ST = (
    (0, 'Pending'),
    (1, 'Accepted'),
    (2, 'Rejected'),
)
MT=(
    (0, '0'),
    (1, '1'),
    (2, '2'),
    (3, '3'),
    (4, '4'),
    (5, '5'),
    (6, '6'),
    (7, '7'),
    (8, '8'),
    (9, '9'),
    (10, '10'),
    (11, '11'),
    (12, '12'),
    (13, '13'),
    (14, '14'),
    (15, '15'),
    (16, '16'),
    (17, '17'),
    (18, '18'),
    (19, '19'),
    (20, '20'),
    (21, '21'),
    (22, '22'),
    (23, '23'),
    (24, '24'),
    (25, '25'),
    (26, '26'),
    (27, '27'),
    (28, '28'),
    (29, '29'),
    (30, '30'),
    (31, '31'),
    (32, '32'),
    (33, '33'),
    (34, '34'),
    (35, '35'),
    (36, '36'),
    (37, '37'),
    (38, '38'),
    (39, '39'),
    (40, '40'),
    (41, '41'),
    (42, '42'),
    (43, '43'),
    (44, '44'),
    (45, '45'),
    (46, '46'),
    (47, '47'),
    (48, '48'),
    (49, '49'),
    (50, '50'),
    (51, '51'),
    (52, '52'),
    (53, '53'),
    (54, '54'),
    (55, '55'),
    (56, '56'),
    (57, '57'),
    (58, '58'),
    (59, '59'),
)
MM = (
    (0, '0'),
    (5, '5'),
    (10, '10'),
    (15, '15'),
    (20, '20'),
    (25, '25'),
    (30, '30'),
    (35, '35'),
    (40, '40'),
    (45, '45'),
    (50, '50'),
    (55, '55'),
)
HH = (
    (1, '1 AM'),
    (2, '2 AM'),
    (3, '3 AM'),
    (4, '4 AM'),
    (5, '5 AM'),
    (6, '6 AM'),
    (7, '7 AM'),
    (8, '8 AM'),
    (9, '9 AM'),
    (10, '10 AM'),
    (11, '11 AM'),
    (12, '12 NOON'),
    (13, '1 PM'),
    (14, '2 PM'),
    (15, '3 PM'),
    (16, '4 PM'),
    (17, '5 PM'),
    (18, '6 PM'),
    (19, '7 PM'),
    (20, '8 PM'),
    (21, '9 PM'),
    (22, '10 PM'),
    (23, '11 PM'),
    (24, '12 AM'),
)

class Attendance(models.Model):
    class Meta:
        ordering = ('-id',)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    event_hh = models.IntegerField(choices=HH, blank=True, null=True)
    event_mm = models.IntegerField(choices=MM, blank=True, null=True)
    event_ss = models.IntegerField(choices=MM, blank=True, null=True)
    event_type = models.IntegerField(choices=IO, blank=True, null=True)
    lattitude = models.DecimalField(decimal_places=2,max_digits=5,null=True)
    longitude = models.DecimalField(decimal_places=2,max_digits=5,null=True)
    fordate = models.DateField(("Date"), default=datetime.date.today)
    address = models.CharField(max_length=300, null=True, blank=True)



class Regularisation(models.Model):
    class Meta:
        ordering = ('-id',)
    branch = models.ForeignKey(Branch,models.SET_NULL,blank=True,null=True)
    employee = models.ForeignKey(Employee,models.SET_NULL,blank=True,null=True)
    date =  models.DateField(("Date"), default=datetime.date.today)
    starttime_hh = models.IntegerField(choices=HH, blank=True, null=True)
    endtime_hh = models.IntegerField(choices=HH, blank=True, null=True)
    starttime_mm= models.IntegerField(choices=MT, blank=True, null=True)
    endtime_mm= models.IntegerField(choices=MT, blank=True, null=True)
    applying_for = models.ForeignKey(WaiverType, models.SET_NULL,blank=True,null=True)
    reason= models.CharField(max_length=100)
    status = models.IntegerField(choices=ST, blank=True, null=True, default=0)





