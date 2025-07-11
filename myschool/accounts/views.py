from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserProfile, School
from .forms import SchoolForm
from django.views.decorators.http import require_POST

from django.http import HttpResponseForbidden


def singup_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        role = request.POST.get('role')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Користувач з таким email вже існує.")
            return redirect('signup')
        
        if password1 != password2:
            messages.eror(request, 'Паролі не співпадають.')
            return redirect('signup')
        
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name
        )

        UserProfile.objects.create(user=user, role=role)
        login(request, user)
        return redirect('profile')
    
    return render(request, 'accounts/signup.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('profile')
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, "Невірні дані.")
            return redirect('login')
        
    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')

@require_POST
@login_required
def edit_account_view(request):
    user = request.user
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    email = request.POST.get('email')

    # Перевірка, чи email вже зайнятий іншим
    if User.objects.filter(email=email).exclude(pk=user.pk).exists():
        messages.error(request, "Користувач з таким email вже існує.")
        return redirect('profile')

    # Оновлення (але НЕ username!)
    user.first_name = first_name
    user.last_name = last_name
    user.email = email
    user.save()

    messages.success(request, "Профіль успішно оновлено.")
    return redirect('profile')

@login_required
@require_POST
def delete_account_view(request):
    user = request.user
    logout(request)
    user.delete()
    messages.success(request, "Акаунт видалено.")
    return redirect('login')

@login_required
def create_school_view(request):
    if not hasattr(request.user, 'userprofile') or request.user.userprofile.role != 'director':
        return HttpResponseForbidden("Тільки директор може створювати школу.")

    if School.objects.filter(director=request.user).exists():
        messages.warning(request, "Ви вже створили школу.")
        return redirect('profile')

    if request.method == 'POST':
        form = SchoolForm(request.POST)
        if form.is_valid():
            school = form.save(commit=False)
            school.director = request.user
            school.save()
            messages.success(request, "Школу створено.")
            return redirect('profile')
    else:
        form = SchoolForm()

    return render(request, 'accounts/create_school.html', {'form': form})