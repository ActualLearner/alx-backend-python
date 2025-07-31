from datetime import datetime
from django.http import JsonResponse
import re


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        user = request.user if request.user.is_authenticated else "Anonymous"
        log_text = f"{datetime.now()} - User: {user} - Path: {request.path}\n"
        with open('./requests.log', 'a') as log:
            log.write(log_text)

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        hour = datetime.now().hour
        restricted_hours = range(6, 9)

        is_conversation_route = (
            re.match(r"^/api/conversations", path) or
            re.match(r"^/api/users/\d+/conversations", path)
        )

        if is_conversation_route and hour in restricted_hours:
            return JsonResponse(
                {"detail": "Messaging is disabled during restricted hours (1AM-6AM)."},
                status=403
            )

        response = self.get_response(request)
        return response
