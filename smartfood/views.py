from django.shortcuts import redirect

def base_redirect(request):
    return redirect('index', permanent=False)