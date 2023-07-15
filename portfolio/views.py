from django.shortcuts import render


def portfolio(request):
    return render(request, 'portfolio/index.html')
