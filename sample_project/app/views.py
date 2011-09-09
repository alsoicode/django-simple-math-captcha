from django.contrib import messages
from django.shortcuts import render

from app.forms import SampleForm


def index(request):
    form = SampleForm(request.POST or None)
    if form.is_valid():
        messages.add_message(request, messages.INFO, 'Form was valid.')
    return render(request, 'index.html', {'form' : form})
