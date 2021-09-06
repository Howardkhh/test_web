from django.db.models.query import QuerySet
from django.shortcuts import render
from django.views.generic import ListView
from .models import Question

# Create your views here.
class FaqListView(ListView):
    template_name = "faq/faq.html"
    queryset = Question.objects.all()