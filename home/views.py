from django.shortcuts import render
from django.views.generic import TemplateView , ListView , CreateView

# Create your views here.
class IndexView(TemplateView):
    template_name='home/inicio.html'