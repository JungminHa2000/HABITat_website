import json
from django.utils.html import json_script
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import *

def all_requests(request):
    request_list = Requests.objects.all()
    return render(request, 'requests.html', {'request_list': request_list})

def all_reports(request):
    report_list = Report.objects.all()
    return render(request, 'reports.html', {'report_list': report_list})

def decline_request(request, req_id):
    declined_req = Requests.objects.get(no_field = req_id)
    declined_req.delete()
    return HttpResponseRedirect(reverse('all_requests'))

def accept_request(request, req_id):
    accepted_req = Requests.objects.get(no_field = req_id)
    tid = accepted_req.task_id
    req = Tasks.objects.get(task_id = tid)
    req.reward = accepted_req.requested_reward
    req.save()
    accepted_req.delete()
    return HttpResponseRedirect(reverse('all_requests'))

def decline_report(request, rep_id):
    declined_rep = Report.objects.get(no_field = rep_id)
    declined_rep.delete()
    return HttpResponseRedirect(reverse('all_reports'))

def accept_report(request, rid):
    delete_user = UserData.objects.get(user_id = rid)
    num_of_reports = UserData.objects.get()
    delete_user.delete()
    delete_reports = Report.objects.get(reportee_id = rid)
    delete_reports.delete()
    goal_id_list = Goals.objects.filter(user_id = rid)

    for goal in goal_id_list.values('goal_id'):
        try:
            delete_goal_info = GoalInfo.objects.get(goal_id = goal['goal_id'])
            delete_goal_info.delete()
        except GoalInfo.DoesNotExist:
            print("GoalInfo matching goal_id of " + str(goal['goal_id'])  + " does not exist")

        try: 
            delete_tasks = Tasks.objects.get(goal_id = goal['goal_id'])
            delete_tasks.delete()
        except Tasks.DoesNotExist:
            print("Tasks matching goal_id of " + str(goal['goal_id'])  + " does not exist")

        try:
            delete_requests = Requests.objects.get(goal_id = goal['goal_id'])
            delete_requests.delete()
        except Requests.DoesNotExist:
            print("Requests matching goal_id of " + str(goal['goal_id']) + " does not exist")
        
    goal_id_list.delete()
    return HttpResponseRedirect(reverse('all_reports'))

def show_all_users(request):
    all_user_list = UserData.objects.all()
    return render(request, 'users.html', {'all_user_list':all_user_list})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')  # Replace 'home' with your desired redirect URL
    else:
        form = AuthenticationForm()

    return render(request, 'Registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')  # Replace 'home' with your desired redirect URL

def visualisation(request):
    goals = GoalInfo.objects.all()
    goals_data = [{'goal_id': goal.goal_id, 'money_in_bank': goal.bank} for goal in goals]
    goals_json_script = json.dumps(goals_data)
    return render(request, 'visualisation.html', {'goals_json_script': goals_json_script})