import json
import uuid

from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse

from App_auth.models import *
from App_auth.forms import *
from App_content.forms import PodcastModelForm
from App_content.models import *
from App_post.models import *
from django.template.loader import get_template

from xhtml2pdf import pisa


# Create your views here.
@login_required(login_url="App_auth:login")
def home(request):
    partnerRequests = PartnerRequestModel.objects.filter(status=True)[:6]
    Jobs = JobPostModel.objects.filter(status=True)[:6]
    userProfile_exist = None
    userProfileExist = None
    post_list = PostsModel.objects.filter(status=True)
    podcastForm = PodcastModelForm()
    userTotalPost = PostsModel.objects.filter(author=request.user).count()
    userTotalPodcast = PodcastModel.objects.filter(host=request.user).count()
    allUsers = CustomUser.objects.filter(is_superuser=False)
    friend_request = ConnectionRequestModel.objects.filter(to_user=request.user)
    totalFriends = ConnectionModel.objects.filter(user=request.user)
    six_users = [x for x in allUsers]
    try:
        loved_post = PostLoveReact.objects.filter(user=request.user)
        loved_post_list = loved_post.values_list('post_id', flat=True)
    except Exception as e:
        loved_post_list = []
    try:
        userProfile_exist = Profile_main.objects.filter(user=request.user).exists()
        if userProfile_exist:
            userProfileExist = 'true'
    except:
        userProfileExist = 'false'

    if request.user.is_authenticated is True and userProfile_exist is False:
        return HttpResponseRedirect(reverse('App_auth:profile-setup'))

    content = {
        'user': request.user,
        'userAuth': None,
        'userProfileExist': userProfileExist,
        'partnerRequests': partnerRequests,
        'postList_first': post_list[:2],
        'postList_second': post_list[2:],
        'allPost': post_list,
        'loved_post_list': loved_post_list,
        'jobs': Jobs,
        'podcastForm': podcastForm,
        'userTotalPost': userTotalPost,
        'userTotalPodcast': userTotalPodcast,
        'six_users': six_users,
        'friend_requestsNotification': friend_request,
        'total_friends': totalFriends,
    }
    if request.user.is_authenticated:
        content['userAuth'] = 'true'
    else:
        content['userAuth'] = 'false'
    # return render(request, 'Basement/home.html', context=content)
    return render(request, 'Home.html', context=content)


def signup_view(request):
    return render(request, 'App_auth/signup_view.html')


def signup_attempt(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password1')
        password2 = request.POST.get('password2')
        try:
            if password2 != password:
                return HttpResponse("Password Doesn't Match")
            if CustomUser.objects.filter(email=email).first():
                return HttpResponse("Email already taken")

            user_obj = CustomUser(email=email)
            user_obj.set_password(password)
            user_obj.save()
            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(user=user_obj, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            return HttpResponse("Token-send")
        except Exception as e:
            return HttpResponse("Error")
    return HttpResponse("Error")


def login_view(request):
    if request.method == 'POST':
        user_email = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(email=user_email, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        return HttpResponse("Failed")
    return render(request, 'App_auth/login_view.html')


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def success(request):
    return render(request, 'App_auth/success.html')


def token_send(request):
    return render(request, 'App_auth/token_send.html')


@login_required
def profile_setup(request):
    if request.method == 'POST':
        # profileModelForm = ProfileModelForm(request.POST, request.FILES)
        # print(profileModelForm.is_valid)
        # if profileModelForm.is_valid():
        #     profile = profileModelForm.save(commit=False)
        #     profile.user = request.user
        fullName = request.POST.get('fullName')
        phone_number = request.POST.get('phone_number')
        Date_of_Birth = request.POST.get('Date_of_Birth')
        house_no = request.POST.get('house_no')
        area = request.POST.get('area')
        city = request.POST.get('city')
        zipcode = request.POST.get('zipcode')
        career_objective = request.POST.get('career_objective')
        gender = request.POST.get('gender')
        ID_card = request.FILES.get('ID_card')
        profile_picture = request.FILES.get('profile_picture')
        profile = Profile_main(user=request.user, fullName=fullName, career_objective=career_objective,
                               phone_number=phone_number, Date_of_Birth=Date_of_Birth, house_no=house_no, area=area,
                               city=city, zipcode=zipcode, gender=gender, ID_card=ID_card,
                               profile_picture=profile_picture)
        profile.save()
        return HttpResponseRedirect(reverse('home'))
    content = {
        # 'profileForm': profileForm
    }
    return render(request, 'App_auth/profile_setup.html', context=content)


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return HttpResponseRedirect(reverse('home'))
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return HttpResponseRedirect(reverse('home'))
        else:
            return HttpResponseRedirect(reverse('App_auth:error'))
    except Exception as e:
        print(e)
        return HttpResponseRedirect(reverse('home'))


def error_page(request):
    return JsonResponse("Error")


def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi, Please click on this link to verify your account http://127.0.0.1:8000/auth/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


@login_required
def profile_view(request):
    profile = Profile_main.objects.get(user=request.user)
    extra_curriculars = Extra_curricular_Activities_Model.objects.filter(user=request.user)
    co_curriculars = Co_curricular_Activities_Model.objects.filter(user=request.user)
    educations = EducationModel.objects.filter(user=request.user)
    experiences = ExperiencesModel.objects.filter(user=request.user)
    skills = SkillListModel.objects.filter(user=request.user)

    add_educations_form = EducationModelForm()
    add_extra_curriculars_form = Extra_curricular_Activities_ModelForm()
    add_co_curriculars_form = Co_curricular_Activities_ModelForm()
    add_experiences_form = ExperiencesModelForm()
    add_skills_form = SkillListModelForm()

    totalFriends = ConnectionModel.objects.filter(user=request.user)
    allPost = PostsModel.objects.filter(author=request.user).order_by("-created_on")
    allPodcast = PodcastModel.objects.filter(host=request.user).order_by("-created_on")
    sumPost = [x for x in allPost] + [x for x in allPodcast]

    content = {
        'profile': profile,
        'extra_curricular': extra_curriculars,
        'co_curricular': co_curriculars,
        'educations': educations,
        'skills': skills,
        'experiences': experiences,
        'add_extra_curriculars_form': add_extra_curriculars_form,
        'add_co_curriculars_form': add_co_curriculars_form,
        'add_educations_form': add_educations_form,
        'add_experiences_form': add_experiences_form,
        'add_skills_form': add_skills_form,
        'totalConnections': totalFriends,
        'sumPost': sumPost
    }
    return render(request, 'App_auth/profileView.html', context=content)


today_day = date.today().day
today_month = date.today().month
today_year = date.today().year


@login_required
def add_new_education(request):
    if request.method == 'POST':
        form = EducationModelForm(request.POST)
        if form.is_valid():
            thisForm = form.save(commit=False)
            thisForm.active = True
            thisForm.user = request.user
            thisForm.save()
            return HttpResponseRedirect(reverse('App_auth:profile-view'))

    return HttpResponseRedirect(reverse('App_auth:profile-view'))


@login_required
def add_new_experience(request):
    if request.method == 'POST':
        form = ExperiencesModelForm(request.POST)
        if form.is_valid():
            thisForm = form.save(commit=False)
            thisForm.user = request.user
            thisForm.save()
            return HttpResponseRedirect(reverse('App_auth:profile-view'))
    return HttpResponseRedirect(reverse('App_auth:profile-view'))


@login_required
def add_new_skill(request):
    if request.method == 'POST':
        form = SkillListModelForm(request.POST)
        if form.is_valid():
            thisForm = form.save(commit=False)
            thisForm.user = request.user
            thisForm.save()
            return HttpResponseRedirect(reverse('App_auth:profile-view'))
    return HttpResponseRedirect(reverse('App_auth:profile-view'))


@login_required
def add_new_extra_curriculum(request):
    if request.method == 'POST':
        form = Extra_curricular_Activities_ModelForm(request.POST)
        if form.is_valid():
            thisForm = form.save(commit=False)
            thisForm.user = request.user
            thisForm.save()
            return HttpResponseRedirect(reverse('App_auth:profile-view'))
    return HttpResponseRedirect(reverse('App_auth:profile-view'))


@login_required
def add_new_co_curriculum(request):
    if request.method == 'POST':
        form = Co_curricular_Activities_ModelForm(request.POST)
        if form.is_valid():
            thisForm = form.save(commit=False)
            thisForm.user = request.user
            thisForm.save()
            return HttpResponseRedirect(reverse('App_auth:profile-view'))
    return HttpResponseRedirect(reverse('App_auth:profile-view'))


@login_required
def general_profile_settings(request):
    return render(request, 'App_auth/settings.html')


@login_required
def password_update(request):
    if request.method == 'POST':
        old_password = request.POST.get('old_password')
        new_password1 = request.POST.get('new_password1')
        new_password2 = request.POST.get('new_password2')
        user = CustomUser.objects.get(id=request.user.id)
        auth_user = authenticate(email=user.email, password=old_password)
        if auth_user:
            user.set_password(new_password1)
            user.save()
            logout(request)
            return HttpResponse("success")


def cv_generate(request):
    profile = Profile_main.objects.get(user=request.user)
    extra_curriculars = Extra_curricular_Activities_Model.objects.filter(user=request.user)
    co_curriculars = Co_curricular_Activities_Model.objects.filter(user=request.user)
    educations = EducationModel.objects.filter(user=request.user)
    experiences = ExperiencesModel.objects.filter(user=request.user)
    skills = SkillListModel.objects.filter(user=request.user)
    achievements = AchievementModel.objects.filter(user=request.user)
    references = ReferencesModel.objects.filter(user=request.user).order_by('-created')[:2]

    referenceModalForm = ReferencesModelForm()

    content = {
        'profile': profile,
        'extra_curricular': extra_curriculars,
        'co_curricular': co_curriculars,
        'educations': educations,
        'skills': skills,
        'experiences': experiences,
        'achievements': achievements,
        'references': references,
        'form': referenceModalForm,
    }
    return render(request, 'App_auth/CV.html', context=content)


def cv_generator_2(request):
    profile = Profile_main.objects.get(user=request.user)
    extra_curriculars = Extra_curricular_Activities_Model.objects.filter(user=request.user)
    co_curriculars = Co_curricular_Activities_Model.objects.filter(user=request.user)
    educations = EducationModel.objects.filter(user=request.user)
    experiences = ExperiencesModel.objects.filter(user=request.user)
    skills = SkillListModel.objects.filter(user=request.user)
    achievements = AchievementModel.objects.filter(user=request.user)
    references = ReferencesModel.objects.filter(user=request.user).order_by('-created')[:2]

    referenceModalForm = ReferencesModelForm()

    content = {
        'profile': profile,
        'extra_curricular': extra_curriculars,
        'co_curricular': co_curriculars,
        'educations': educations,
        'skills': skills,
        'experiences': experiences,
        'achievements': achievements,
        'references': references,
        'form': referenceModalForm,
    }
    return render(request, 'App_auth/CV_alternative.html', context=content)


def add_reference(request):
    ref = ReferencesModel.objects.filter(user=request.user)
    refList = [x.name_of_reference for x in ref]
    if request.method == 'POST':
        form = ReferencesModelForm(request.POST)
        referenceName = request.POST.get('name_of_reference')
        if referenceName in refList:
            return HttpResponseRedirect(reverse('App_auth:cv-open'))
        if form.is_valid():
            thisForm = form.save(commit=False)
            thisForm.user = request.user
            thisForm.save()
            return HttpResponseRedirect(reverse('App_auth:cv-open'))

    return HttpResponseRedirect(reverse('App_auth:profile-view'))


def pdf_generator(request):
    profile = Profile_main.objects.get(user=request.user)
    extra_curriculars = Extra_curricular_Activities_Model.objects.filter(user=request.user)
    co_curriculars = Co_curricular_Activities_Model.objects.filter(user=request.user)
    educations = EducationModel.objects.filter(user=request.user)
    experiences = ExperiencesModel.objects.filter(user=request.user)
    skills = SkillListModel.objects.filter(user=request.user)
    achievements = AchievementModel.objects.filter(user=request.user)
    references = ReferencesModel.objects.filter(user=request.user).order_by('-created')[:2]

    template_path = 'App_auth/downloadablePDF.html'
    context = {
        'profile': profile,
        'extra_curricular': extra_curriculars,
        'co_curricular': co_curriculars,
        'educations': educations,
        'skills': skills,
        'experiences': experiences,
        'achievements': achievements,
        'references': references,
    }
    # Create a Django response object, and specify content_type as pdf
    response = HttpResponse(content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="{request.user}-CV.pdf"'
    response['Content-Disposition'] = f'filename="{request.user}-CV.pdf"'
    # find the template and render it.
    template = get_template(template_path)
    html = template.render(context)

    # create a pdf
    pisa_status = pisa.CreatePDF(
        html, dest=response)
    # if error then show some funny view
    if pisa_status.err:
        print("Error")
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response
