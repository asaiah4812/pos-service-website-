from django.http import HttpResponseForbidden

def verified_user_only(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_verified:
            return view_func(request, *args, **kwargs)
        else:
            return HttpResponseForbidden("You are not authorized to access this page.")
    return wrapper