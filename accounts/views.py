from django.shortcuts import render
from django.views.generic import View, TemplateView


class AccountsHome(TemplateView):
    template_name = 'accounts/dashboard.html'
