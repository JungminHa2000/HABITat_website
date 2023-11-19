import json
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from .models import *
from django.db import transaction
from django.db.models import Q
from django.core.mail import send_mail
from django.http import HttpResponseRedirect
from collections import Counter

# Returns all the requests
def all_requests(request):
    request_list = Requests.objects.filter(admin_responded=0)
    request_all = Requests.objects.all()
    return render(request, 'requests.html', {'request_list': request_list, 'request_all': request_all})

# Returns all the reports
def all_reports(request):
    report_list = Report.objects.filter(admin_responded=0)
    report_all = Report.objects.all()
    return render(request, 'reports.html', {'report_list': report_list, 'report_all': report_all})

# Returns the counts of different stats to display a summary in the dashboard screen
def home_summary(request):
    report_count = Report.objects.filter(admin_responded=0).count()
    request_count = Requests.objects.count()
    user_count = UserData.objects.count()
    goal_count = GoalInfo.objects.count()
    banned_user_count = UserData.objects.filter(banned=1).count()

    report_dates = Report.objects.values_list('date_reported', flat=True)
    date_counts = Counter(date.strftime('%Y-%m-%d') for date in report_dates)
    request_dates = Requests.objects.values_list('date_requested',flat=True)
    date_counts2 = Counter(date.strftime('%Y-%m-%d') for date in request_dates)
    # Extract unique dates and their counts
    unique_dates = list(date_counts.keys())
    report_counts = list(date_counts.values())

    unique_dates2 = list(date_counts2.keys())
    request_counts = list(date_counts2.values())

    return render(request, 'webHome.html', {'unique_dates2': unique_dates2, 'request_counts': request_counts, 'unique_dates': unique_dates,
        'report_counts': report_counts, 'report_count': report_count, 'request_count': request_count, 'user_count': user_count, 'goal_count': goal_count, 'banned_user_count': banned_user_count})

# Returns the reports by reportee username
def get_reportee_reports(request, reportee):
    reports = Report.objects.get(reportee_username=reportee)
    return render(request, 'reports.html', {'reports': reports})

# Returns all the goals and task infomation about all the users
def user_info(request, user_id):
    user_goals = Goals.objects.filter(user=user_id)
    goal_list = []

    for goal in user_goals:
        goal_info = GoalInfo.objects.get(goal_id=goal.goal_id)

        goal_details = {
            'goal_id': goal.goal_id,
            'goal_desc': goal_info.goal_desc,
            'bank': goal_info.bank,
            # Add other fields from GoalInfo table as needed
        }

        tasks = Tasks.objects.filter(goal=goal.goal_id)
        task_list = []

        for task in tasks:
            task_details = {
                'task_id': task.task_id,
                'task_desc': task.task_desc,
                'reward': task.reward,
                # Add other fields from Tasks table as needed
            }
            task_list.append(task_details)

        goal_details['tasks'] = task_list
        goal_list.append(goal_details)
    user = UserData.objects.get(user_id=user_id)
    username = user.user_name

    users = UserData.objects.filter(banned=0)  # Retrieve all users who are not banned
    user_ids = [user.user_id for user in users]  # Extract user IDs

    return render(request, 'user_info.html', {'goal_list': goal_list, 'username': username, 'user_ids': user_ids})

# Logic to decline a reward change request
def decline_request(request, req_id):
    declined_req = Requests.objects.get(no_field=req_id)
    declined_req.admin_responded = 1
    declined_req.save()
    return HttpResponseRedirect(reverse('all_requests'))

# Logic to accpet a reward change request
def accept_request(request, req_id):
    accepted_req = Requests.objects.get(no_field=req_id)
    tid = accepted_req.task_id
    req = Tasks.objects.get(task_id=tid)
    req.reward = accepted_req.requested_reward
    req.save()
    accepted_req.admin_responded = 1
    accepted_req.save()
    return HttpResponseRedirect(reverse('all_requests'))

# Logic to decline a report
def decline_report(request, rep_id):
    report = Report.objects.get(no_field=rep_id)
    report.admin_responded = 1
    report.save()
    return HttpResponseRedirect(reverse('all_reports'))

# Logic to accept a report
def accept_report(request, rep_id):
    report = Report.objects.get(no_field=rep_id)
    report.admin_responded = 1
    report.save()
    user = UserData.objects.get(user_id=report.reportee_id)
    user.num_reported += 1
    user.save()
    try:
        with transaction.atomic():
            delete_user = UserData.objects.get(user_id=report.reportee_id)
            user_email = delete_user.email
            num_reported = delete_user.num_reported
            user_name = delete_user.user_name
            delete_all_reports = Report.objects.filter(reportee_id=delete_user.user_id)

            if num_reported > 3:
                subject = 'You are banned'
                msg = 'Dear {}, \n \n You have been warned 3 times. Your account will be removed. \n \n Have a good day, \n HABITat Team'.format(user_name)
                delete_all_reports.delete()

                goal_id_list = Goals.objects.filter(user_id=report.reportee_id)

                for goal in goal_id_list:
                    goal_id = goal.goal_id
                    GoalInfo.objects.filter(goal_id=goal_id).delete()
                    Tasks.objects.filter(goal=goal_id).delete()
                    Requests.objects.filter(
                        Q(goal=goal_id) | Q(task_id=goal_id)).delete()
                    
                delete_user.banned = 1
                delete_user.save()

                goal_id_list.delete()

            if num_reported == 3:
                subject = 'Final warning'
                msg = 'Dear {}, \n \n This is your final warning. Next time, you will be banned. Please be mindful of other users and be kind to yourself. \n \n Have a good day, \n HABITat Team'.format(user_name)

            if num_reported == 2:
                subject = 'Strike Two'
                msg = 'Dear {}, \n \n Please be mindful of other users and be kind to yourself. If you think there was a mistake, please report it. \n \n Have a good day, \n HABITat Team'.format(user_name)

            if num_reported == 1:
                subject = 'Strike One'
                msg = 'Dear {}, \n \n Please be mindful of other users and be kind to yourself. If you think there was a mistake, please report it. \n \n Have a good day, \n HABITat Team'.format(user_name)

    except UserData.DoesNotExist:
        print("User not found.")

    send_mail(
        subject,
        msg,
        'HABITat.cs4500@gmail.com',
        [user_email],
        fail_silently=False,
    )
    return HttpResponseRedirect(reverse('all_reports'))

# Logic to delete a user
def delete_user(request, uid):
    try:
        with transaction.atomic():
            delete_user = UserData.objects.get(user_id=uid)
            delete_reports = Report.objects.filter(reportee_id=uid)
            delete_reports.delete()

            goal_id_list = Goals.objects.filter(user_id=uid)

            for goal in goal_id_list:
                goal_id = goal.goal_id
                GoalInfo.objects.filter(goal_id=goal_id).delete()
                Tasks.objects.filter(goal=goal_id).delete()
                Requests.objects.filter(
                    Q(goal=goal_id) | Q(task_id=goal_id)).delete()

            goal_id_list.delete()
            delete_user.delete()
            delete_reports.delete()
    except UserData.DoesNotExist:
        print("User not found.")
    return HttpResponseRedirect(reverse('show_all_users'))

# Returns all the users
def show_all_users(request):
    all_user_list = UserData.objects.all()
    not_banned = UserData.objects.filter(banned=0)
    return render(request, 'users.html', {'all_user_list': all_user_list, 'not_banned': not_banned})

# Logic for logging in
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'Registration/login.html', {'form': form})

# Logic for logging out
def logout_view(request):
    logout(request)
    return redirect('home')

# Logic for graph data returning for the graph page
def visualisation(request):
    goals = GoalInfo.objects.all()
    goals_data = [{'goal_id': goal.goal_id, 'money_in_bank': goal.bank}
                  for goal in goals]
    goals_json_script = json.dumps(goals_data)

    reports = Report.objects.all()
    reporter_reportees = {}
    for report in reports:
        reporter_id = report.reporter_id
        reportee_id = report.reportee_id
        reportee_username = report.reportee_username

        if reporter_id not in reporter_reportees:
            reporter_reportees[reporter_id] = []

        reporter_reportees[reporter_id].append(
            {'id': reportee_id, 'username': reportee_username})

    tree_data = []
    for reporter_id, reportees in reporter_reportees.items():
        reporter_username = Report.objects.filter(
            reporter_id=reporter_id).first().reporter_username
        reporter = {
            'id': reporter_id,
            'username': reporter_username,
            'children': reportees
        }
        tree_data.append(reporter)

    context = {
        'goals_json_script': goals_json_script,
        'tree_data': json.dumps(tree_data),
    }

    return render(request, 'visualisation.html', context)
