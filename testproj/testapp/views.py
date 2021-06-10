from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
# Create your views here.
def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.validate(request.POST)
    if errors:
        for e in errors.values():
            messages.error(request, e)
        return redirect('/')
    else:
        new_user = User.objects.register(request.POST)
        request.session['user_id'] = new_user.id
        messages.success(request, "You have successfully registered!")
        return redirect('/success')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not User.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid Email/Password')
        return redirect('/')
    user = User.objects.get(email=request.POST['email'])
    request.session['user_id'] = user.id
    messages.success(request, "You have successfully logged in!")
    return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

# def google(request):
#     request.session.clear()
#     # return redirect('/')
#     return redirect('/')    

def success(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user
    }
    return render(request, 'success.html', context)

# start of stock views.py code

def google(request):
    context = {
        'shows': Stock.objects.all()
    }
    return render(request, 'stocks.html', context)

def new(request):
    return render(request, 'new.html')

def create(request):
    # CREATE THE SHOW
    errors = Stock.objects.validate(request.POST)
    if errors:
        for (key, value) in errors.items():
            messages.error(request, value)
        return redirect('/shows/new')

    Stock.objects.create(
        title = request.POST['title'],
        network = request.POST['network'],
        release_date = request.POST['release_date'],
        description = request.POST['description']
    )
    return redirect('/shows')

def edit(request, show_id):
    one_show = Stock.objects.get(id=show_id)
    context = {
        'show': one_show
    }
    return render(request, 'edit.html', context)

def update(request, show_id):
    # update show!
    to_update = Stock.objects.get(id=show_id)
    # updates each field
    to_update.title = request.POST['title']
    to_update.release_date = request.POST['release_date']
    to_update.network = request.POST['network']
    to_update.description = request.POST['description']
    to_update.save()

    return redirect('/shows/')

def show(request, show_id):
    # query for one show with show_id
    one_show = Stock.objects.get(id=show_id)
    context = {
        'show': one_show
    }
    return render(request, 'stock.html', context)

def delete(request, show_id):
    # NOTE: Delete one show!
    to_delete = Stock.objects.get(id=show_id)
    to_delete.delete()
    return redirect('/shows')

def add_like(request, id):
    print(‘ID:’, id)
    liked_stock = Stock.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_stock.user_likes.add(user_liking)
    return redirect('/stocks')
    