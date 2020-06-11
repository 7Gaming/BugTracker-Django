from django.shortcuts import render
from .models import Bug
from .forms import SubmitBugForm, ChangeStatusForm
from django.utils import timezone
from enum import Enum

# Create your views here.

def main(request):
    #Establish a dictionary that will be sent to the template html
    context = {
        'form': SubmitBugForm(),
        'open': Bug.objects.filter(status="open"),
        'progress': Bug.objects.filter(status="progress"),
        'closed': Bug.objects.filter(status="closed"),
        'error_msg': "Unknown error"
    }
    #Create a variable to represent each form that may have been filled out (Submiting a bug or changing its status)
    bug_report = SubmitBugForm(request.POST or None)
    status_change = ChangeStatusForm(request.POST or None)
    #If the user is submitting a bug report
    if bug_report.is_valid():
        data = bug_report.cleaned_data
        #By default return an error and don't reset the form
        context['error'] = True
        context['form'] = bug_report
        if len(data['name']) > 30:
            context['error_msg'] = "The name you entered is longer than 30 characters"
        elif len(Bug.objects.filter(name=data['name'])) != 0:
            context['error_msg'] = "A bug already exists by this name"
        elif len(data['description']) > 5000:
            context['error_msg'] = "The description you entered is longer than 5,000 characters (" + str(len(data['description'])) + ")"
        elif len(Bug.objects.filter(description=data['description'])) != 0:
            context['error_msg'] = "A bug already exists with this description"
        else:
            #If the data is fit to enter the database then remove the default error and add it to the database
            context['error'] = False
            context['form'] = SubmitBugForm()
            Bug(name=data['name'], description=data['description'], status="open", open_time=timezone.now()).save()
        print(data)
    #If the user is submitting a status change
    elif status_change.is_valid():
        data = status_change.cleaned_data
        #If the bug exists in the database (by name) and the user has submitted a valid status to change it to
        if len(Bug.objects.filter(name=data['name'])) == 1 and data['status'] in ["open", "progress", "closed"]:
            rows = Bug.objects.filter(name=data['name'])
            #If the new status is "closed" then add a closed_time / If the new status is "open" then remove the previous closed_time
            if data['status'] == "closed":
                rows.update(closed_time=timezone.now())
            elif data['status'] == "open":
                rows.update(closed_time=None)
            rows.update(status=data['status'])
        print(data)
    #Catch any errors that may occur when submitting data and log them to the console
    elif request.method == "POST":
        context['error'] = True
        context['form'] = bug_report
        print(str(bug_report.errors) + "\n\n" + str(status_change.errors))
    #This will fire if the user is just now arriving at the website ('GET')
    else:
        print("New webpage request")
    #Render the dynamic html
    return render(request, 'bugtracker.html', context)
