from taxis.models import *
from django.shortcuts import render_to_response, get_object_or_404, redirect
from django import forms
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
import datetime

# home -- View for Home Page
# Renders a response to home.html, with an instance of TaxiForm
def home(request):
    form = TaxiForm()
    return render_to_response('taxis/home.html', {'form': form}, 
    context_instance=RequestContext(request))

# index -- Index Page
# Renders every single taxi in the database
def index(request):
    taxiList = Taxi.objects.all()
    return render_to_response('taxis/index.html', {'taxiList': taxiList})
    
# about -- About Page
# Renders response to static document
def about(request):
    return render_to_response('taxis/about.html')
    
# displayTaxis -- Displays all taxis with the same endlocation (don't think this works)
# This assumes that startLoc, endLoc, and startTime are all valid!
def displayTaxis(startLoc, endLoc, startTime):
    taxisToEndLoc = Taxi.objects.filter(endLoc=endLoc)
    return render_to_response('taxis/index.html', {'taxiList': taxisToEndLoc})
    
# manageTaxiRequest -- Handles a search from the home page
# If the form is valid, it checks for an exact match. If found, it goes to that taxi page. 
# Later, it should actually add the user to the taxi. Else, if a close match exists (same endLocation and date),
# then it returns a list of taxis that match that. If no match exists, a taxi is created.
def manageTaxiRequest(request):
    if request.method == 'POST':
        form = TaxiForm(request.POST)
        if form.is_valid():
            startLoc = form.cleaned_data['startLoc']
            endLoc = form.cleaned_data['endLoc']
            startTime = form.cleaned_data['startTime']
            # IF EXACT MATCH EXISTS, go to that taxi page
            try:
                exactMatch = Taxi.objects.filter(endLoc=endLoc).filter(startLoc=startLoc)[0]
                alert = "Exact match found!"
                return redirect(detail, taxi_id=exactMatch.id)
                # Improve later so that it chooses the one with the most passengers
            except IndexError: # Taxi doesn't exist
                # IF CLOSE MATCH EXISTS (same endLoc + date)
                # See all taxis with that endLoc and date
                year = startTime.year
                month = startTime.month
                day = startTime.day
                closeMatches = Taxi.objects.filter(startTime__year=year, startTime__month=month,
                startTime__day=day, endLoc = endLoc)
                if closeMatches:
                    alert = "Showing close matches..."
                    return render_to_response('taxis/index.html', {'taxiList': closeMatches, 'alert': alert})
                # OTHERWISE create a new taxi
                else:
                    t = Taxi(startLoc=startLoc, endLoc=endLoc, startTime=startTime)
                    t.save()
                    alert = "No match, so we started a taxi for you. You will be notified when someone joins."
                    return HttpResponseRedirect('/taxis/' + str(t.id), {'alert': alert})
        else:
            form = TaxiForm()
        
        # why is this here?
        return render_to_response('taxis/index.html', {
            'form': form,
        }, context_instance=RequestContext(request))
    
def detail(request, taxi_id):
    taxi = get_object_or_404(Taxi, pk=taxi_id)
    if request.method == 'POST': #Passenger was added
        form = PassForm(request.POST)
        if form.is_valid():
            #Add passenger to taxi
            firstName = form.cleaned_data['firstName']
            lastName = form.cleaned_data['lastName']
            email = form.cleaned_data['email']
            newPass = Passenger(firstName=firstName, lastName=lastName, email=email)
            newPass.save()
            taxi.passengers.add(newPass)
            taxi.save()
            return HttpResponseRedirect('/taxis/' + taxi_id)
        else:
            form = PassForm()
            
    else:
         form = PassForm()   
    
    return render_to_response('taxis/detail.html', {'taxi': taxi, 'form': form,},
    context_instance=RequestContext(request))

def addTaxi(request):
    if request.method == 'POST':
        form = TaxiForm(request.POST)
        if form.is_valid():
            # Add taxi to database
            startLoc = form.cleaned_data['startLoc']
            endLoc = form.cleaned_data['endLoc']
            startTime = form.cleaned_data['startTime']
            t = Taxi(startLoc=startLoc, endLoc=endLoc, startTime=startTime)
            t.save()
            
            return HttpResponseRedirect('/taxis/')
    else:
        form = TaxiForm()
    
    return render_to_response('taxis/add.html', {
        'form': form,
    }, context_instance=RequestContext(request))
