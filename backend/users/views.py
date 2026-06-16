from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import authenticate, login, logout

def register(request):

    if request.method == 'POST':

        form = RegisterForm(request.POST)

        if form.is_valid():

            form.save()

            print("USER CREATED SUCCESSFULLY")

            return redirect('/login')

        else:
            print(form.errors)

    else:
        form = RegisterForm()

    return render(
        request,
        'users/register.html',
        {'form': form}
    )
def login_view(request):

    if request.method == 'POST':

        username = request.POST.get('username')
        password = request.POST.get('password')

        print("USERNAME:", username)
        print("PASSWORD:", password)

        user = authenticate(
            request,
            username=username,
            password=password
        )

        print("USER FOUND:", user)

        if user:
            login(request, user)
            return redirect('/')

        return render(
            request,
            'users/login.html',
            {'error': 'Invalid username or password'}
        )

    return render(request, 'users/login.html')