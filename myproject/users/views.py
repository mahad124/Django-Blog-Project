from multiprocessing import context
from django.shortcuts import render, redirect
from django.contrib import messages 
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpadateForm

def register(request):
    if request.method == 'POST': 
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! Now you can Login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def profile(request):
    print("User from middleware:", request.user)
    print("Is authenticated:", request.user.is_authenticated)
    print("Session data:", request.session.items())
    if request.method == 'POST': 
        u_form = UserUpdateForm(request.POST,instance=request.user)
        p_form = ProfileUpadateForm(request.POST,
                                    request.FILES,
                                    instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been Updated!')
            return redirect('profile') 

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpadateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'users/profile.html', context)


def logout_success(request):
    """Shown after logout; LogoutView redirects here (Django 5+ never renders a template)."""
    return render(request, 'users/logout.html')


# messages.debug
# messages.info
# messages.success
# messages.warning
# messages .error 