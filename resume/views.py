from django.shortcuts import render,redirect
from django.contrib import messages
from users.models import User
from .models import Resume
from .form import UpdateResumeForm
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required
def update_resume(request):
    if request.user.is_applicant:
        resume = Resume.objects.get(user=request.user)
        if request.method == 'POST':
            form = UpdateResumeForm(request.POST, request.FILES, instance=resume)
            if form.is_valid():
                var = form.save(commit=False)
                user = User.objects.get(id=request.user.id)
                user.has_resume = True
                var.save()
                user.save()
                messages.info(request,'Your Resume info has been updated')
                return redirect('dashboard')
            else:
                messages.warning(request,'Something went wrong')
        else:
            form = UpdateResumeForm(instance=resume)
            context = {'form':form}
            return render(request,'resume/update_resume.html',context)
    messages.warning(request,'Permission Dined')
    return redirect('dashboard')

@login_required
def resume_details(request,pk):
    resume = Resume.objects.get(pk=pk)
    context = {'resume':resume}
    return render(request,'resume/resume_details',context)
