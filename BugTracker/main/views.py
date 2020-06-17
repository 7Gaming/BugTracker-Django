from django.shortcuts import render
from .models import Bug
from .forms import SubmitBugForm, ChangeStatusForm
from django.utils import timezone
from django.views import View

class MainView(View):
    #Establish a dictionary that will be sent to the template html
    context = { }

    #Used to update the list of bugs in the context list
    def update_context(self):
        self.context = {
            'form': SubmitBugForm(),
            'open': Bug.objects.filter(status="open"),
            'progress': Bug.objects.filter(status="progress"),
            'closed': Bug.objects.filter(status="closed")
        } 

    def validate_bug_report(self, bug_report):
        data = bug_report.cleaned_data
        print(data)
        if len(data['name']) > 30:
            return (True, "The name you entered is longer than 30 characters", bug_report)
        elif len(Bug.objects.filter(name=data['name'])) != 0:
            return (True, "A bug already exists by this name", bug_report)
        elif len(data['description']) > 5000:
            return (True, "The description you entered is longer than 5,000 characters (" + str(len(data['description'])) + ")", bug_report)
        elif len(Bug.objects.filter(description=data['description'])) != 0:
            return (True, "A bug already exists with this description", bug_report)
        else:
            #If the data is fit to enter the database then add it and return a fitting tuple
            Bug(name=data['name'], description=data['description'], status="open", open_time=timezone.now()).save()
            return (False, None, SubmitBugForm())
        

    def validate_status_change(self, status_change):
        data = status_change.cleaned_data
        print(data)
        #If the bug exists in the database (by name) and the user has submitted a valid status to change it to
        if len(Bug.objects.filter(name=data['name'])) == 1 and data['status'] in ["open", "progress", "closed"]:
            rows = Bug.objects.filter(name=data['name'])
            #If the new status is "closed" then add a closed_time / If the new status is "open" then remove the previous closed_time
            if data['status'] == "closed":
                rows.update(closed_time=timezone.now())
            elif data['status'] == "open":
                rows.update(closed_time=None)
            rows.update(status=data['status'])
            #Update context so that the user will have immediate feedback
            self.update_context()

    #Used to render a page
    def load_page(self, request, page):
        print("New webpage request (" + page + ")")
        return render(request, page, self.context)

    #When a user goes to the page without posting data
    def get(self, request):
        self.update_context()
        return self.load_page(request, 'bugtracker.html')
    
    #When the user posts data to the server
    def post(self, request):
        self.update_context()
        #Create a variable to represent each form that may have been filled out (Submiting a bug or changing its status)
        bug_report = SubmitBugForm(request.POST)
        status_change = ChangeStatusForm(request.POST)
        #If the user is submitting a bug report call the validation definition and set the context variables to match the response
        if bug_report.is_valid():
            self.context['error'], self.context['error_msg'], self.context['form'] = self.validate_bug_report(bug_report)
        #If the user is submitting a status change
        elif status_change.is_valid():
            self.validate_status_change(status_change)
        return self.load_page(request, 'bugtracker.html')