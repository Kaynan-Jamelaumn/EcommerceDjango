from django.shortcuts import render


def portfolio(request):
    return render(request, 'portfolio/index.html')


def portfolioEn(request):
    return render(request, 'portfolio/portfolioeng.html')
