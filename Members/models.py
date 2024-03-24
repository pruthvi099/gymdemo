from django.db import models
from Accounts.models import User
from Plans.models import Plan
from django.urls import reverse

# Create your models here.

class Enquiry(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    birthday = models.DateField()
    # rejected = models.BooleanField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'{self.name} - {self.location}'

class Member(models.Model):
    name = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    birthday = models.DateField()

    is_enquiry = models.BooleanField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    plan_validity = models.BooleanField(null=True, blank=True)
    enquiry = models.ForeignKey(Enquiry, on_delete=models.CASCADE, null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.name} - {self.location}'
    

class MemberPlan(models.Model):
    is_active = models.BooleanField(null=True, blank=True)
    is_paid = models.BooleanField(null=True, blank=True)

    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, null=True, blank=True)
    member = models.ForeignKey(Member, on_delete=models.CASCADE, null=True, blank=True)

    startdate = models.DateField(null=True, blank=True)
    enddate = models.DateField(null=True, blank=True)
    paymentdate = models.DateField(null=True, blank=True)

    created = models.DateTimeField(auto_now_add=True)
    createdby = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return f'{self.member} - {self.plan}'