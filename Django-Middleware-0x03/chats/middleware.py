from datetime import datetime, timedelta
import logging
from django.http import HttpResponseForbidden, JsonResponse

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

        # configuring the logger
        self.logger = logging.getLogger(__name__)
        handler = logging.FileHandler("request_logs.txt")
        formatter = logging.Formatter("%(message)s")
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __call__(self, request, **kwds):
        user = request.user
        message = f"{datetime.now()} - User: {user} - Path: {request.path}"
    

        self.logger.info(message)

        response = self.get_response(request)

        return response
    


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, **kwds):
        user = request.user

        if (datetime.now().hour != 6) or (datetime.now().hour != 21) :
            return HttpResponseForbidden(                "Access to the messaging app is restricted between 9PM and 6AM.")

        response = self.get_response(request)

        return response
    
class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_log = {}
        self.time_window = timedelta(minutes=1)
    
    def get_client_ip(self, request):
        """Helper function to extract IP address"""
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')
    
    def __call__(self, request, **kwds):
        # Get client IP
        ip = self.get_client_ip(request)

        # Only monitor POST requests (i.e., message sends)
        if request.method == "POST":
            now = datetime.now()

            # Get the list of timestamps for this IP
            if ip not in self.request_log:
                self.request_log[ip] = []

            # Remove timestamps older than 1 minute
            self.request_log[ip] = [
                t for t in self.request_log[ip] if now - t < self.time_window
            ]

            # Check if the IP has exceeded the limit
            if len(self.request_log[ip]) >= 5:
                return JsonResponse(
                    {"error": "Message limit exceeded. Please wait a minute."},
                    status=429,
                )

            # Otherwise, log this new request
            self.request_log[ip].append(now)

        # Continue processing
        return self.get_response(request)



        response = self.get_response(request)

        return response
    
    
class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        

    def __call__(self, request, **kwds):
        # Only apply if user is authenticated
        if request.user.is_authenticated:
            user_role = getattr(request.user, 'role', None)       

            if user_role not in ["admin", "moderator"]:
                return JsonResponse(
                    {"error": "Forbidden: You do not have permission to access this resource."},
                    status=403,
                )

        # Proceed normally
        return self.get_response(request)