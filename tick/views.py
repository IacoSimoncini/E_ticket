from logging import raiseExceptions

from django.db.models.expressions import Expression
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
from .decorators import unauthenticated_user, allowed_users, admin_only, profile
from django.db.models import F
import tick.contracts.smart_contract as sc
import tick.utils as utils
import traceback


w3 = sc.start_web3()
abi = sc.read_abi("tick/contracts/abi_event.json")
bytecode = sc.read_bytecode("tick/contracts/bytecode_event.json")

w3.eth.default_account = w3.eth.accounts[0]
contract_event_not_deployed = sc.create_contract(abi, bytecode, w3)

def events(request):
    events = Event.objects.exclude(num_ticket=0)
    total_events = events.count()

    film= events.filter(category='Cinema')
    sport= events.filter(category='Sport')
    teatro= events.filter(category='Teatro')
    concerti= events.filter(category='Concerti')

    context= {'events':events, 'total_events':total_events, 'film':film, 'sport':sport, 'teatro':teatro, 'concerti':concerti }

    return render(request,'tick/home.html', context)


@login_required(login_url='login')
@profile
def userPage(request):
    events = Event.objects.all()
    total_events = events.count()

    for e in events:
        contract_deployed=sc.deploy_contract(e.address, abi, w3)
        temp_tick = sc.getTickets(contract_deployed, request.user.last_name) 
        if len(temp_tick) == 0:
            events = events.exclude(id=e.id)

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

    
    utils.setup(w3, abi)
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

def error(request):

    context = {}
    return render(request, 'tick/accounts/error.html', context)

@login_required(login_url='login')
@admin_only
def createEvent(request):
    
    form = EventForm()
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        
        if form.is_valid():
            prezzo = float(request.POST['prezzo']) * 100
            prezzo = int(prezzo)
            print('prezzo: ', prezzo)
            try:
                form=form.save()
                tx_hash,tx_receipt=sc.hash_receipt(contract_event_not_deployed, w3, form.id, int(request.POST['num_ticket']), request.POST['nome'], request.POST['luogo'], prezzo)           
                contract_event=sc.deploy_contract(tx_receipt.contractAddress, abi, w3)
                #tx_receipt=w3.eth.wait_for_transaction_receipt(contract_event)
                EventForm.Meta.model.objects.filter(pk=form.id).update(address=tx_receipt.contractAddress)
                
            except Exception:
                print(traceback.format_exc())
                EventForm.Meta.model.objects.filter(pk=form.id).delete()
                return redirect ('/tick/error/')
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
            try:
                evento = EventForm.Meta.model.objects.get(id=pk)
                contract_event = sc.deploy_contract(evento.address, abi, w3)
                prezzo = float(request.POST['prezzo']) * 100
                prezzo = int(prezzo)
                contract_address =sc.update_contract(contract_event,int(request.POST['num_ticket']),request.POST['nome'],request.POST['luogo'],prezzo,w3)
                EventForm.Meta.model.objects.filter(pk=pk).update(address=contract_address)
                form.save()
            except Exception:
                print(traceback.format_exc())
                return redirect ('/tick/error/')
            return redirect ('/tick/manager/')

    context={'form':form}
    return render(request, 'tick/accounts/create_event.html', context)


@login_required(login_url='login')
@admin_only
def deleteEvent (request,pk):

    event=Event.objects.get(id=pk)
    if request.method == 'POST':
        try:
            contract_event=sc.deploy_contract(event.address, abi, w3)
            sc.delete_event(contract_event,int(pk),w3)
            event.delete()
        except:
            return redirect ('/tick/error/')
        return redirect ('/tick/manager/')
    context={'item':event}  #item l'ho chiamato in delete.html
    return render(request, 'tick/accounts/delete.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def buyTicket (request,pk):
    ticket= Event.objects.get(id=pk)
    if request.method == 'POST':
        try:
            if ticket.num_ticket != 0:
                contract_event=sc.deploy_contract(ticket.address, abi, w3)
                contract_address =sc.buy_ticket(contract_event, request.user.last_name, w3)
                #EventForm.Meta.model.objects.filter(pk=pk).update(address=contract_address)
                ticket.address = contract_address
                ticket.num_ticket-=1
                ticket.save()
                #ticket = sc.getTickets(contract_event, request.user.last_name)
            else:
                messages.error(request, 'No tickets available')
        except Exception:
            print(traceback.format_exc())
            return redirect ('/tick/error/')
        return redirect ('home')
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
    
    try:
        ticket= Event.objects.get(id=pk)

        purchased = Event.objects.exclude(address=0)
        total_purchased=purchased.count()

        purchased_cinema=purchased.filter(category='Cinema')
        purchased_sport=purchased.filter(category='Sport')
        purchased_teatro=purchased.filter(category='Teatro')
        purchased_concerti=purchased.filter(category='Concerti')

        contract_deployed=sc.deploy_contract(ticket.address, abi, w3)
    
        Users = list(User.objects.exclude(last_name=""))
    
        tickets = []

        for user in Users:
            tick = sc.getTickets(contract_deployed, user.last_name)

            if type(tick) is list:
                for t in tick:
                    if t[2] == True:
                        t += (user.username, user.id, pk, )
                        tickets.append(t)
    except Exception:
        print(traceback.format_exc())
        return redirect ('/tick/error/')

    context={'tickets': tickets, 'ticket':ticket, 'purchased_cinema':purchased_cinema, 'purchased_sport':purchased_sport,'purchased_teatro':purchased_teatro, 'purchased_concerti':purchased_concerti, 'purchased':purchased, 'total_purchased':total_purchased}
    return render(request, 'tick/accounts/manage_ticket.html',  context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def manageBuy(request,pk):
    ticket= Event.objects.get(id=pk)

    contract_deployed = sc.deploy_contract(ticket.address, abi, w3)
    temp_tick = sc.getTickets(contract_deployed, request.user.last_name)
    tickets=[]
    for i,tick in enumerate(temp_tick):
        tick+=(i,)
        tickets.append(tick)

    context= {'tickets':tickets ,'id_evento':pk,'id_user':request.user.id, 'name_event': ticket.nome}
    return render(request,'tick/accounts/managebuy.html', context)

@login_required(login_url='login')
def invalidateTicket(request, pk, id_evento, id_user):

    user = User.objects.get(id=id_user)

    item = (pk, id_evento, id_user, user.username, )
    
    if request.method == 'POST':
        try:
            event= Event.objects.get(id=id_evento)
            contract_deployed=sc.deploy_contract(event.address, abi, w3)
            temp_tick = sc.getTickets(contract_deployed, user.last_name)
            result = False
            for i, tick in enumerate(temp_tick):
                if tick[1] == int(pk) and tick[2] == True:
                    result =sc.invalidation(contract_deployed, user.last_name, int(i), w3)
                    break
            if not result:
                messages.error(request, 'Ticket has been invalidated yet')
                return redirect ('/tick/manage_ticket/' + id_evento + '/')
        except Exception:
            print(traceback.format_exc())
            return redirect ('/tick/error/')
        return redirect ('/tick/manage_ticket/' + id_evento + '/')
    
    context = {'item': item}
    return render(request, 'tick/accounts/confirm_inv.html', context)

@login_required(login_url='login')
def refundTicket(request, pk, id_evento, id_user):

    item = (pk, id_evento, id_user, )
    event= Event.objects.get(id=id_evento)

    if request.method == 'POST':
        try:
            user= User.objects.get(id=id_user)
            contract_deployed=sc.deploy_contract(event.address, abi, w3)
            result =sc.refundTicket(contract_deployed, user.last_name, int(pk), w3)
            if result:
                num_ticket=event.num_ticket+1
                Event.objects.filter(pk=id_evento).update(num_ticket=num_ticket)
            else:
                messages.error(request, 'No ticket to refund')
                return redirect ('/tick/refund/' + pk + '/' + id_evento + '/' + id_user)
        except Exception:
            print(traceback.format_exc())
            return redirect ('/tick/error/')
        return redirect ('/tick/managebuy/' + id_evento + '/')
    
    context = {'item': item, 'event': event}
    return render(request, 'tick/accounts/confirm_ref.html', context)
    
    
  