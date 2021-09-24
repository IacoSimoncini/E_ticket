from .models import Tick, Event
from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.
from .forms import EventForm, CreateUserForm
from django.contrib.auth.models import User, Group
from django.contrib import messages
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.db.models import F
import tick.contracts.smart_contract as sc

w3 = sc.start_web3()
abi = sc.read_abi("tick/contracts/abi_event.json")
bytecode = sc.read_bytecode("tick/contracts/bytecode_event.json")

w3.eth.default_account = w3.eth.accounts[0]
contract_event_not_deployed = sc.create_contract(abi, bytecode, w3)

def events(request):
    events = Event.objects.all()
    total_events = events.count()

    film= events.filter(category='Cinema')
    sport= events.filter(category='Sport')
    teatro= events.filter(category='Teatro')
    concerti= events.filter(category='Concerti')

    context= {'events':events, 'total_events':total_events, 'film':film, 'sport':sport, 'teatro':teatro, 'concerti':concerti }

    return render(request,'tick/home.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    events = Event.objects.all()
    total_events = events.count()

    film= events.filter(category='Cinema')
    sport= events.filter(category='Sport')
    teatro= events.filter(category='Teatro')
    concerti= events.filter(category='Concerti')

    context= {'events':events, 'total_events':total_events, 'film':film, 'sport':sport, 'teatro':teatro, 'concerti':concerti }

    return render(request,'tick/accounts/user.html', context)

def contattaci(request):
    return render(request,'tick/contattaci.html')


@unauthenticated_user
def registerPage(request):
    form= CreateUserForm()
    if request.method == 'POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            address, private_key = sc.create_account(w3)
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            messages.success(request, 'Account created for ' + username)
            CreateUserForm.Meta.model.objects.filter(pk=user.id).update(last_name=address)
            return redirect ('login')

    context = {'form': form}
    return render (request, 'tick/accounts/register.html', context)


@unauthenticated_user
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password =request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            if user.groups.filter(name='customer'):
                return redirect('home')
            if user.groups.filter(name='reseller'):
                return redirect('reseller-page')
            else: 
                return redirect('manager')
        else:
            messages.info(request, 'Username OR password is incorrect')

    context = {}
    return render(request, 'tick/accounts/login.html', context)


@login_required(login_url='login')
def logoutUser(request):
	logout(request)
	return redirect('login')


@login_required(login_url='login')
@admin_only
def managerPage(request):
    #category= Event.category.all()

    events = Event.objects.all()
    total_events = events.count()

    film= events.filter(category='Cinema')
    sport= events.filter(category='Sport')
    teatro= events.filter(category='Teatro')
    concerti= events.filter(category='Concerti')


    context= {'events':events, 'total_events':total_events, 'film':film, 'sport':sport, 'teatro':teatro, 'concerti':concerti }

    return render(request, 'tick/accounts/manager.html',  context)


@login_required(login_url='login')
@admin_only
def createEvent(request):
    
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        
        if form.is_valid():
            
            form=form.save()   
            
            tx_hash,tx_receipt=sc.hash_receipt(contract_event_not_deployed, w3, form.id, int(request.POST['num_ticket']), request.POST['nome'], request.POST['luogo'], int(request.POST['prezzo']))           
            contract_event=sc.deploy_contract(tx_receipt.contractAddress, abi, w3)
            EventForm.Meta.model.objects.filter(pk=form.id).update(address=tx_receipt.contractAddress)
            return redirect ('/tick/manager/')

    context={'form':form}

    return render(request, 'tick/accounts/create_event.html', context)


@login_required(login_url='login')
@admin_only
def updateEvent(request, pk):
    
    event=Event.objects.get(id=pk)
    
    form = EventForm(instance=event)
    
    if request.method == 'POST':
        
        form = EventForm(request.POST, request.FILES, instance=event)
        
        if form.is_valid():
            evento=EventForm.Meta.model.objects.get(id=pk)
            reduction=evento.num_ticket-int(request.POST['num_ticket'])
            contract_event=sc.deploy_contract(evento.address, abi, w3)
            if(reduction<=sc.getTicketAvaiable(contract_event)):
                #inserire messaggio d'avviso
                form.save()
                tx_receipt=sc.update_contract(contract_event,int(request.POST['num_ticket']),request.POST['nome'],request.POST['luogo'],int(request.POST['prezzo']),w3)
                EventForm.Meta.model.objects.filter(pk=pk).update(address=tx_receipt)
                return redirect ('/tick/manager/')

    context={'form':form}
    return render(request, 'tick/accounts/create_event.html', context)


@login_required(login_url='login')
@admin_only
def deleteEvent (request,pk):

    event=Event.objects.get(id=pk)
    if request.method == 'POST':
        event.delete()
        sc.delete_event(pk)
        return redirect ('/tick/manager/')
    context={'item':event}  #item l'ho chiamato in delete.html
    return render(request, 'tick/accounts/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def buyTicket (request,pk):
    ticket= Event.objects.get(id=pk)
    if request.method == 'POST':
        ticket.num_ticket-=1
        ticket.save()
        contract_event=sc.deploy_contract(ticket.address, abi, w3)
        tx_receipt=sc.buy_ticket(contract_event, request.user.last_name, w3)
        EventForm.Meta.model.objects.filter(pk=pk).update(address=tx_receipt)
           
        return redirect ('/tick/user/')
    context={'ticket':ticket}  #'ticket' l'ho chiamato in confirm.html
    return render(request, 'tick/accounts/confirm.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['reseller'])
def resellerPage(request):
    events = Event.objects.all()
    total_events = events.count()


    film= events.filter(category='Cinema')
    num_film=film.count()

    sport= events.filter(category='Sport')
    num_sport=sport.count()

    teatro= events.filter(category='Teatro')
    num_teatro=teatro.count()

    concerti= events.filter(category='Concerti')
    num_concerti=concerti.count()

    context={'events':events, 'total_events':total_events, 'film':film, 'sport':sport, 'teatro':teatro, 'concerti':concerti, 
    'num_film':num_film, 'num_teatro':num_teatro, 'num_sport':num_sport, 'num_concerti':num_concerti}
    return render(request, 'tick/accounts/reseller.html',  context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['reseller'])
def manageTicket(request,pk):
    context={}
    return render(request, 'tick/accounts/manage_ticket.html',  context)
