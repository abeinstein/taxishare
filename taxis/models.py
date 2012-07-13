from django.db import models
from django import forms


# Create your models here.
class Passenger(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    
    def __unicode__(self):
        return self.firstName + " " + self.lastName

class Taxi(models.Model):
    startLoc = models.CharField(max_length=100)
    endLoc = models.CharField(max_length=100)
    startTime = models.DateTimeField()
    passengers = models.ManyToManyField(Passenger)
    
    def __unicode__(self):
        return "Taxi to " + self.endLoc + " at " + str(self.startTime)
        
class TaxiForm(forms.Form):
    startLoc = forms.CharField(max_length=100, label='Start Location')
    endLoc = forms.CharField(max_length=100, label='End Location')
    startTime = forms.DateTimeField(label="Date and Time")

class PassForm(forms.Form):
    firstName = forms.CharField(max_length=50, label='First Name')
    lastName = forms.CharField(max_length=50, label='Last Name')
    email = forms.EmailField(label='Email')
