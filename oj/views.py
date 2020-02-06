from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def index(request):
    print(request.path)
    return render(request, 'index.html')


@login_required()
def dashboard(request):
    print(request.path)
    return render(request, 'oj/dashboard.html')


@login_required()
def assignment(request):
    return render(request, 'oj/assignments.html')
