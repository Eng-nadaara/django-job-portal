from django.http import HttpResponseForbidden
from django.shortcuts import render,redirect
from jobcreate.models import Job,ApplyJob
from .filter import JobFilter
from django.contrib import messages

# Create your views here.
def home(request):
    filter = JobFilter(request.GET,queryset=Job.objects.filter(is_available=True).order_by('-timestamp'))
    context = {'filter':filter}
    return render(request,'website/home.html',context)


# def can_view_job(fuction):
#     def wrapper()

def job_listing(request):
    if request.user.is_authenticated:
        user =  request.user
        perms_code = "jobcreate.view_job"

        has_perms = user.has_perm(perms_code)
        if has_perms:
            jobs = Job.objects.filter(is_available=True).order_by('-timestamp')
            context = {'jobs':jobs}
            return render(request,'website/job_listing.html',context)
        else:
            messages.warning(request,'Permision Dinied Job Listings')
            return redirect('home')
    return redirect('login')
       
        
        


def job_details(request,pk):
    if ApplyJob.objects.filter(user=request.user.id, job=pk).exists():
        has_applied = True
    else:
        has_applied = False
    job = Job.objects.get(pk=pk)
    context = {'job':job,'has_applied':has_applied}
    return render(request,'website/job_details.html',context)