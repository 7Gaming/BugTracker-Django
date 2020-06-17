from django.shortcuts import render

# Create your views here.

def main(request):
    return render(request, 'bugtracker.html')

def add_bug(request):
    name = request.POST['name']
    desc = request.POST['desc']

    return render(request, 'bugtracker.html', {'name': name})



'''
open = []
for x in range(15):
    open.append("Bug " + str(x))
progress = []
for x in range(6):
    progress.append("Bug " + str(x))
fixed = []
for x in range(3):
    fixed.append("Bug " + str(x))
'''