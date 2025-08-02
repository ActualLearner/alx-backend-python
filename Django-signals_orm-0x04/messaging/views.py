from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_page
from messaging.models import Message, Notification

# Create your views here.


@login_required
def delete_user(self, request):
    user = request.user
    logout(request)

    user.delete()
    return redirect('home')


@cache_page(60) # Cache for 60 seconds
def get_messages(self, request):
    sent_messages = Message.objects.filter(
        sender=request.user).select_related('parent_message')
    received_messages = Message.objects.filter(
        receiver=request.user).select_related('parent_message')
    return JsonResponse({
        "sent_messages": sent_messages,
        "received_messages": received_messages,
    }, status=200)


def get_unread_messages(self, request):
    unread_messages = Message.unread.unread_for_user(
        request.user).only('id', 'sender', 'timestamp', 'content')
    return JsonResponse({"messages": unread_messages}, status=200)
