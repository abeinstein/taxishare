from taxis.models import *
from django.shortcuts import render_to_response, get_object_or_404
from django import forms
from django.template import RequestContext
from django.http import HttpResponseRedirect

def home(request):
    form = TaxiForm()
    return render_to_response('taxis/home.html', {'form': form}, 
    context_instance=RequestContext(request))

def index(request):
    taxiList = Taxi.objects.all()
    return render_to_response('taxis/index.html', {'taxiList': taxiList})
    
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
