from django.shortcuts import render

#a simple index view
def index(request):
    return render(request, 'main/index.html')
