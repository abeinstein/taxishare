from django.db import models
from django import forms
from django.forms import ModelForm


# Create your models here.
class Passenger(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)
    email = models.EmailField()
    
    def __unicode__(self):
        return self.firstName + " " + self.lastName

class Taxi(models.Model):
    START_LOC_CHOICES = (
        ('South', 'South Campus (SCRH)'),
        ('Reg', "Regenstein Library (57th b/w Ellis and Uni)"),
        ('Ratner', "Ratner Athletic Center (55th and Ellis)"),
        ('Stony', "Stony Island (57th and Stony)"),
        ('Ida', "Ida Noyes (59th and Woodlawn)"),
        ('Kim', "Kimbark Plaza (53rd and Woodlawn)")
    )
    
    END_LOC_CHOICES = (
        ('Oha', "O'Hare International Airport"),
        ('Mid', "Midway International Airport"),
        ('Uni', "Union Station")
    )
    
    startLoc = models.CharField("Start Location", max_length=100, 
        choices=START_LOC_CHOICES,
        )
    
    endLoc = models.CharField("End Location", max_length=100, choices=END_LOC_CHOICES)
    startTime = models.DateTimeField("Date/Time")
    passengers = models.ManyToManyField(Passenger)
    
    def __unicode__(self):
        return "Taxi from " + self.startLoc + " to " + self.endLoc + " at " + str(self.startTime)

class TaxiForm(ModelForm):
    class Meta:
        model = Taxi
        exclude = ('passengers',)
        
        def __init__(self, *args, **kwargs):
            super(TaxiForm, self).__init__(*args, **kwargs)
            
        
class PassForm(ModelForm):
    class Meta:
        model = Passenger


