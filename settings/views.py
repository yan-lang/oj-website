from django.contrib.auth.decorators import login_required
from django.shortcuts import render


@login_required()
def user_profile(request):
    return render(request, 'settings/profile.html')


@login_required()
def account(request):
    return render(request, 'settings/account.html')
