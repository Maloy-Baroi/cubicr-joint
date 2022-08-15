from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, HttpResponseRedirect, reverse

# Create your views here.
from django.utils.translation import gettext_lazy

from App_auth.models import CustomUser
from App_chat.models import Room
from App_post.forms import JobPostModelForm, JobApplyForm
from App_post.models import PartnerRequestModel, JobPostModel, PartnerApplicationModel, JobApplicationModel


@login_required
def partner_request_view(request):
    partner_requests = PartnerRequestModel.objects.filter(status=True)
    return render(request, "App_post/display_partner_request.html", {"partner_request": partner_requests})


@login_required
def my_project_n_partner_view(request):
    my_pnr = PartnerRequestModel.objects.filter(author=request.user, status=True)
    content = {
        'my_pnr': my_pnr,
    }
    return render(request, 'App_post/my_research_projects_view.html', context=content)



@login_required
def partner_request_form_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        groupName = request.POST.get('groupName')
        participants = int(request.POST.get('total_participants'))
        location = request.POST.get('location')
        activity_type = request.POST.get('type')
        duration = request.POST.get('project_duration')
        skills = request.POST.get('required_skills')
        deadline = request.POST.get('application_deadline')
        file = request.FILES.get('related_file')
        description = request.POST.get('description')
        request_model = PartnerRequestModel(title=title, groupName=groupName, type=activity_type,
                                            total_participants=participants,
                                            project_duration=duration, location=location,
                                            author=request.user, required_skills=skills,
                                            application_deadline=deadline, related_file=file, description=description)
        request_model.save()
        room = Room(name=groupName)
        room.save()
        grp = Group.objects.get_or_create(name=groupName)
        grp[0].user_set.add(request.user)
        return HttpResponseRedirect(reverse('App_post:partner-request'))
    return HttpResponseRedirect(reverse('home'))


@login_required
def apply_for_participation(request, pk):
    partnerRequest = PartnerRequestModel.objects.get(id=pk)
    applications = PartnerApplicationModel.objects.filter(activity=partnerRequest)
    project = PartnerRequestModel.objects.get(id=pk)
    if request.method == 'POST':
        reason = request.POST.get('reason')
        apply_model = PartnerApplicationModel(activity=project, participant=request.user,
                                              reason_of_participation=reason)
        apply_model.save()
        return HttpResponseRedirect(reverse('home'))
    content = {
        'project': project,
        'applications': applications,
    }
    return render(request, 'App_post/apply_for_participation.html', context=content)


@login_required
def display_job_list(request):
    jobs = JobPostModel.objects.filter(status=True)
    content = {
        'jobs': jobs
    }
    return render(request, 'App_post/display_job_list.html', context=content)


@login_required
def job_post(request):
    form = JobPostModelForm()
    if request.method == 'POST':
        form = JobPostModelForm(request.POST)
        if form.is_valid():
            thisForm = form.save(commit=False)
            thisForm.author = request.user
            thisForm.save()
            return HttpResponseRedirect(reverse('home'))
    return render(request, 'App_post/job_post.html', context={'form': form})


@login_required
def single_job_view(request, pk):
    job = JobPostModel.objects.get(id=pk)
    applications = JobApplicationModel.objects.filter(applied_job=job, candidate=request.user)
    applied = applications.exists()
    form = JobApplyForm()
    content = {
        'job': job,
        'applied': applied,
        'form': form,
    }
    return render(request, 'App_post/single_job_post.html', context=content)


@login_required
def apply_for_job(request, pk):
    job = JobPostModel.objects.get(id=pk)
    if request.method == 'POST':
        form = JobApplyForm(request.POST)
        if form.is_valid():
            thisForm = form.save(commit=False)
            thisForm.candidate = request.user
            thisForm.applied_job = job
            thisForm.status = True
            thisForm.save()
            return HttpResponseRedirect(reverse('App_post:single-job-post', kwargs={'pk': pk}))

    return HttpResponseRedirect(reverse('App_post:single-job-post', kwargs={'pk': pk}))


def accept_apply_for_research_participation(request, user_id, pnr_apply_id):
    pnr_application = PartnerApplicationModel.objects.get(id=pnr_apply_id)
    pnr = PartnerRequestModel.objects.get(id=pnr_application.activity.id)
    user = CustomUser.objects.get(id=user_id)
    print(pnr_application)
    pnr_application.status = True
    pnr_application.save()
    grp = pnr.groupName
    print(grp)
    findGrp = Group.objects.get(name=grp)
    findGrp.user_set.add(user)
    return HttpResponseRedirect(reverse('App_post:apply-for-participation', kwargs={'pk': pnr_application.activity.id}))



