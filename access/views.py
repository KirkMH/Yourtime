from django.shortcuts import render

from django.contrib.auth.decorators import login_required


@login_required
def dashboard(request):
    context = {
        'greeting': 'Hello, there!',
        'clients': 0,
        'open_jo': 0,
        'due_jo': 0,
    }
    return render(request, 'dashboard.html', context)
