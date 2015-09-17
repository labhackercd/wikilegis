from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from wikilegis.auth2.forms import SignUpForm


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            password = form.cleaned_data['password1']
            user = authenticate(username=user.email, password=password)
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', context=dict(
        form=form,
    ))
