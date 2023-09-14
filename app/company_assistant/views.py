from django.shortcuts import render

from django.http import HttpResponse


def employer_page(request):
    return HttpResponse("Hello, world. You're at employer's page.")

