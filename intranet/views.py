from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django import forms
from django.contrib.auth import authenticate, login, logout

Message = lambda request, msg: render(request, 'message.html', {'msg': msg})

def index(request):
    return render(request, 'index.html')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)


def loginView(request):
    redirectUrl = request.GET.get('next') or '/'
    if request.method == 'POST': # If the form has been submitted...
        form = LoginForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect(redirectUrl) # Redirect after POST
                else:
                    return Message(request, 'Your account has been disabled!')
            else:
                return Message(request, 'Your username and password were wrong')

    else:
        form = LoginForm() # An unbound form

    return render(request, 'login.html', {
        'form': form,
    })


def logoutView(request):
    logout(request)
    return Message(request, 'Logged out!')

