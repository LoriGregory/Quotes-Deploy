from __future__ import unicode_literals
from .models import User
from .models import Quote
from django.shortcuts import render, redirect
from django.contrib import messages

def index(request):
    return render(request, 'quotables/index.html')

def register(request):
    result = User.objects.validate_registration(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    return redirect('/quotables.quotes.html')

def login(request):
    result = User.objects.validate_login(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    request.session['user_id'] = result.id
    return redirect('/quotables.quotes.html')

def user(request):
    try:
        request.session['user_id']
    except KeyError:
        return redirect('/')
    #need to get alias for User_id (also need # of posts made)
    context = {
            'alias':User.objects.get(id=request.session['user_id'])
    }
    context = {

     Quote.objects.get(id=request.session['user_id']).favorite_quotes([Quote.objects.order_by(created).last([2])
    }
    return render(request, '/quotables.user.html', context)

def create(request): 
    #for the quotables page.
    #need to show 3 most recent posts, validate and add user's favorites
    result = User.objects.validate_create(request.POST)
    if type(result) == list:
        for err in result:
            messages.error(request, err)
        return redirect('/')
    return redirect('/quotables.quotes.html')

    context = {
        'user': User.objects.get(id=request.session['user_id'])
    }
    for quote in Quote.objects.get(user_id={}).favorite_quotes.all().order_by(created_at).last()[:3]:
    return render(request, '/quotables.user.html', context)

def remove (request):
       
        return render(request,'quotables/users.html')

def logout(request):
    #need to clear session and go back to login page(index)
    for key in request.session.keys():
        del request.session[key]
    return redirect('/')

