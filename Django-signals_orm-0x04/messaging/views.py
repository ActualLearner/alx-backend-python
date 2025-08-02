from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def delete_user(self, request):
    user = request.user
    logout(request)
    
    user.delete()
    return redirect('home')