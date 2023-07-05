from django.shortcuts import render ,HttpResponse

def hello(r):

    return render(r,'hello.html', {'user':'Ahmed'})