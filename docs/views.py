from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

@login_required
def home(request):
    return render(request, 'home.html')

def login(request):
    if request.method == 'POST':
        return HttpResponseRedirect(reverse('simple-sso-login'))
    return render(request, 'login.html')
