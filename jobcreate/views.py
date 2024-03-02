from django.http import HttpResponseForbidden
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages

from .models import Job,ApplyJob
from .form import CreateJobForm,UpdateJobForm
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required


#create a job
@login_required
def create_job(request):
    if request.user.is_authenticated and request.user.is_recruiter:
        if request.user.is_recruiter and request.user.has_company:
             user1 =  request.user
             perms_code = "jobcreate.add_job"

             has_perms = user1.has_perm(perms_code)
             if has_perms:
                if request.method == 'POST':
                    form = CreateJobForm(request.POST)
                    if form.is_valid():
                        var = form.save(commit=False)
                        var.user = request.user
                        var.company = request.user.recruiter
                        var.save()
                        messages.info(request,'New job has been created.')
                        return redirect('dashboard')
                    else:
                        messages.warning(request,'Something went wrong')
                        return redirect('create-job')
                else:
                    form = CreateJobForm()
                    context = {'form':form}
                    return render(request,'job/create_job.html',context)
             else:
                messages.warning(request,'Permision Dinied To Add Ajob')
                return redirect('dashboard')
                

        else:
            messages.warning(request,'permision Denied')
            return redirect('dashboard')
    else:
        messages.info(request,'Please login to Continue')
        return redirect('login')
    
@login_required
def update_job(request,pk):
     if request.user.is_authenticated and request.user.is_recruiter:
        user1 =  request.user
        perms_code = "jobcreate.change_job"

        has_perms = user1.has_perm(perms_code)
        if has_perms:
            job = Job.objects.get(pk=pk)
            if request.method == 'POST':
                form = UpdateJobForm(request.POST, instance=job)
                if form.is_valid():
                    form.save()
                    messages.info(request,'Your job info is updated.')
                    return redirect('dashboard')
                else:
                    messages.warning(request,'Something went wrong')
                    return redirect('update-job')
            else:
                form = UpdateJobForm(instance=job)
                context = {'form':form}
                return render(request,'job/update_job.html',context)
        else:
            messages.warning(request,'Permision Dinied To Update Ajob')
            return redirect('dashboard')  
     else:
        messages.info(request,'Please login to Continue')
        return redirect('login')






    
#manage job for joobsekeers only
@login_required
def manage_job(request):
        user1 =  request.user
        perms_code = "jobcreate.view_job"

        has_perms = user1.has_perm(perms_code)
        if has_perms:
            jobs = Job.objects.filter(user=request.user, company=request.user.recruiter)
            context ={'jobs':jobs}
            return render(request,'job/manage_job.html',context)
        else:
            messages.warning(request,'Permision Dinied To Manage Ajob')
            return redirect('dashboard') 
     


@login_required
def delete_job(request,pk):
     job_to_delete = get_object_or_404(Job, id=pk)
     if job_to_delete.user == request.user and job_to_delete.company == request.user.recruiter:
        job_to_delete.delete()
        messages.success(request, 'Job deleted successfully.')
        return redirect('manage-jobs')
     else:
        messages.warning(request, 'Permission Denied to delete this job.')
        return redirect('manage-jobs')   
  

@login_required
def apply_to_job(request,pk):
    if request.user.is_authenticated and request.user.is_applicant:
        user1 =  request.user
        perms_code = "jobcreate.add_applyjob"

        has_perms = user1.has_perm(perms_code)
        if has_perms:
            job = Job.objects.get(pk=pk)
            if ApplyJob.objects.filter(user=request.user, job=pk).exists():
                messages.warning(request,'Permission Denied')
            else:
                ApplyJob.objects.create(
                    job=job,
                    user=request.user,
                    status = 'Accepted'
                )
                messages.info(request,'You have Successfully applied! please see Home')
                subject = 'Job Application Confirmation'
                message = 'Thank you for applying to the job. Your application is Accepted review.'
                from_email = 'djangoabdullahi@gmail.com'
                to_email = [request.user.email]

                send_mail(subject, message, from_email, to_email, fail_silently=False)
                return redirect('home')
        else:
            messages.warning(request,'Permision Dinied To Apply Ajob')
            return redirect('home')  
    else:
        messages.info(request,'Please login to Continue')
        return redirect('login')


def all_applicants(request,pk):
    # user =  request.user
    # perms_code = "view_job"

    # has_perms = user.has_perm(perms_code)
    # if has_perms:
        job = Job.objects.get(pk=pk)
        applicants = job.applyjob_set.all()
        context = {'job':job,'applicants':applicants}
        return render(request,'job/all_applicants.html',context)
    # return HttpResponseForbidden("lama ogala")

# manage applied Jobs for users
@login_required
def applied_jobs(request):
    user1 =  request.user
    perms_code = "jobcreate.view_applyjob"

    has_perms = user1.has_perm(perms_code)
    if has_perms:
        jobs = ApplyJob.objects.filter(user=request.user)
        context = {'jobs':jobs}
        return render(request,'job/applied_job.html',context)
    else:
         messages.warning(request, 'Permission Denied to Manage Applied job.')
         return redirect('dashboard')  