from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
from datetime import datetime

def index(request):
    if 'logged_in' not in request.session:
        request.session['logged_in'] = False
    return render(request, "webapp/index.html")

def register(request):
    errors = User.objects.RegValidator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        print('*' * 30 + 'Registration attempt error messages: ')
        return redirect('/')

    else:
        print('*' * 30 + 'No registration errors.')
        pwhash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt() )
        User.objects.create(
            name = request.POST['name'],
            username = request.POST['username'],
            password = pwhash,
        )
        user = User.objects.last()
        request.session['logged_in'] = True
        request.session['id'] = user.id
        return redirect('/dashboard')
        
def create(request):
    errors = Wish.objects.WishValidator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/new')
    
    else:
        wish = Wish.objects.create(
            item = request.POST['item'],
            creator = User.objects.get(id=request.session['id']),
        )
        print('*'*40 +'else statement running')
        return redirect('/dashboard')
        
def login(request):
    errors = {}
    login_attempt = User.objects.filter(username = request.POST['username'])
    if len(login_attempt) == 0:
        errors['username'] = "Invalid login."
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    elif not bcrypt.checkpw(request.POST['password'].encode(), login_attempt[0].password.encode()):
        errors['username'] = "Invalid login."
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(username = request.POST['username'])
        request.session['logged_in'] = True
        request.session['id'] = login_attempt[0].id
        return redirect('/dashboard')

def logout(request):
    request.session.clear()
    request.session['logged_in'] = False
    return render(request, "webapp/index.html")

def new(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['id'])
    }
    return render(request, 'webapp/create.html', context)

def saved(request, id):
    if 'id' not in request.session:
        return redirect('/')
    context =  {
        'wish': Wish.objects.get(id = id),
    }
    return render(request, 'webapp/savers.html', context)

def dashboard(request):
    if 'id' not in request.session:
        return redirect('/')
    context = {
        'user': User.objects.get(id=request.session['id']),
        'wish': Wish.objects.filter(savers = User.objects.get(id=request.session['id'])),
        'savers': Wish.objects.exclude(savers = User.objects.get(id=request.session['id']))
    }
    print(context['user'])
    return render(request, 'webapp/dashboard.html', context)

def remove(request, id):
    toremove = Wish.objects.get(id=id)
    currentuser=User.objects.get(id=request.session['id'])
    toremove.savers.remove(currentuser)
    toremove.save()
    return redirect('/dashboard')

def add(request, id):
    toadd = Wish.objects.get(id=id)
    currentuser = User.objects.get(id=request.session['id'])
    toadd.savers.add(currentuser)
    toadd.save()
    return redirect('/dashboard')

def delete(request, id):
    todelete = Wish.objects.get(id=id)
    currentuser = User.objects.get(id=request.session['id'])
    if todelete.creator == currentuser:
        todelete.delete()
        return redirect('/dashboard')
    else:
        return redirect('/dashboard')
        