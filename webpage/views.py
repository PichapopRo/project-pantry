from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import login
from webpage.forms import CustomRegisterForm


def recipes(request):
    return render(request, 'recipes/recipe.html')


def register_view(request):
    if request.method == 'POST':
        form = CustomRegisterForm(request.POST)
        if form.is_valid():
            password = form.cleaned_data.get('password')
            password_confirm = form.cleaned_data.get('password_confirm')

            # Validate password length
            if len(password) < 8:
                messages.error(request, "Password must be at least 8 "
                                        "characters long")
                return render(request, 'registration/signup.html',
                              {'form': form})

            # Validate password match
            if password != password_confirm:
                messages.error(request, "Passwords do not match")
                return render(request, 'registration/signup.html',
                              {'form': form})

            # If everything is fine, create the user
            user = form.save(commit=False)
            user.set_password(password)
            user.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('home')  # Redirect to home or another page
    else:
        form = CustomRegisterForm()

    return render(request, 'registration/signup.html', {'form': form})
