from django.contrib import messages
from django.shortcuts import redirect, render
from .models import *
# Create your views here.
def home(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        option = request.POST.get('option')
        room_code = request.POST.get('room_code')
        if(option == '1'):
            try:
                game = Game.objects.get(room_code=room_code)    
                return redirect(f'/play/{room_code}/{username}/')
                
            except Game.DoesNotExist:
                messages.error(request, 'Room does not exist')
                return redirect('/')
                
        elif(option == '2'):
            if(Game.objects.filter(room_code=room_code).exists()):
                messages.error(request, 'Room already exists')
                return redirect('/')
            else:
                game = Game.objects.create(room_code=room_code) 
                return redirect(f'/play/{room_code}/{username}/')

            
    return render(request, 'home.html')



def play(request , code, username):

    try:
        game = Game.objects.get(room_code=code)
    except Game.DoesNotExist:
        messages.error(request, 'Room does not exist')
        return redirect('/')
    return render(request, 'play.html' , {'username':username, 'code':code})