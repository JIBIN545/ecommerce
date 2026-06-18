from django.http import HttpResponse

from django.shortcuts import render

# def admin_required(fun):
#     def wrapper(request):
#         if request.user.is_superuser == False:
#             return HttpResponse("Admin User Only")
#         else:
#             return fun(request)
#
#     return wrapper

from django.contrib import messages
def admin_required(fun):
    def wrapper(request):
        if request.user.is_superuser == False:
            messages.error(request,"You are not allowed to do that")
            return render(request,'error.html')
        else:
            return fun(request)
    return wrapper