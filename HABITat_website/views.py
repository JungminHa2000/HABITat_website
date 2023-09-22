from django.shortcuts import render
from .models import Requests
from .models import Report
from .models import Tasks, UserData

def all_requests(request):
    request_list = Requests.objects.all()
    return render(request, 'requests.html', {'request_list': request_list})

def all_reports(request):
    report_list = Report.objects.all()
    return render(request, 'reports.html', {'report_list': report_list})

def decline_request(request, req_id):
    declined_req = Requests.objects.get(no_field = req_id)
    declined_req.delete()
    return render(request, 'requests.html')

def accept_request(request, req_id):
    accepted_req = Requests.objects.get(no_field = req_id)
    tid = accepted_req.task_id
    req = Tasks.objects.get(task_id = tid)
    req.reward = accepted_req.requested_reward
    req.save()
    accepted_req.delete()
    return render(request, 'requests.html')

def decline_report(request, rep_id):
    declined_rep = Report.objects.get(no_field = rep_id)
    declined_rep.delete()
    return render(request, 'reports.html')

def show_all_users(request):
    all_user_list = UserData.objects.all()
    return render(request, 'users.html', {'all_user_list':all_user_list})
