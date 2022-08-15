from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse

from App_chat.models import Room
from App_content.forms import SyllabusModelForm
from App_content.models import *


# Create your views here.

@login_required
def new_podcast(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        cover_image = request.FILES.get('cover_image')
        audio_file = request.FILES.get('podcastFile')
        description = request.POST.get('description')
        audio_model = PodcastModel(host=request.user, title=title, description=description, cover_image=cover_image,
                                   audio_file=audio_file)
        audio_model.save()
        return HttpResponseRedirect(reverse('home'))
    return HttpResponseRedirect(reverse('home'))


@login_required
def podcast_listview(request):
    pod_list = PodcastModel.objects.filter(status=True)
    categorical_podcast = {'Stories': [], 'Education': [], 'Music': [], 'Coding': [], 'Science': [], 'Motivation': [],
                           'Life & Goal': [], 'Business & Technology': [], 'Art & Culture': [], 'Health & Sports': []}
    for i in pod_list:
        categorical_podcast[i.categories].append(i)
    for i in categorical_podcast:
        for j in categorical_podcast[i]:
            print(j)
    content = {
        'categorical_podcast': zip(categorical_podcast.keys(), categorical_podcast.values()),
    }
    return render(request, 'App_content/podcast_listview.html', context=content)


@login_required
def new_post(request):
    if request.method == 'POST':
        post_title = request.POST.get('topic_name')
        my_content = request.POST.get('my-content')
        image1 = request.FILES.get('image_1')
        image2 = request.FILES.get('image_2')
        image3 = request.FILES.get('image_3')

        post_model = PostsModel(author=request.user, topic_name=post_title, post_image1=image1, post_image2=image2,
                                post_image3=image3, my_text=my_content, status=True)
        post_model.save()
        return HttpResponseRedirect(reverse('home'))
    return HttpResponseRedirect(reverse('home'))


@login_required
def post_listview(request):
    post_list = PostsModel.objects.filter(status=True)
    content = {
        'post_list': post_list,
    }
    return render(request, 'App_content/post_listview.html', context=content)


@login_required
def post_love(request, pk):
    post = get_object_or_404(PostsModel, id=pk)
    print(post)
    already_loved = PostLoveReact.objects.filter(post=post, user=request.user)
    if not already_loved.exists():
        print("not exist")
        like_post = PostLoveReact(post=post, user=request.user)
        like_post.save()
        return HttpResponseRedirect(reverse('home'))


@login_required
def post_no_loved(request, pk):
    post = PostsModel.objects.get(id=pk)
    already_loved = PostLoveReact.objects.filter(post=post, user=request.user)
    already_loved.delete()
    return HttpResponseRedirect(reverse('home'))


@login_required
def make_post_status_false(request, pk):
    post = PostsModel.objects.get(id=pk)
    post.status = False
    post.save()
    return HttpResponse("Post Removed, It won't show from the next time")


@login_required
def make_pod_status_false(request, pk):
    pod = PodcastModel.objects.get(id=pk)
    pod.status = False
    pod.save()
    return HttpResponse("Post Removed, It won't show from the next time")


# -----------------------------syllabus--------------------------------------------#

def add_syllabus(request):
    if request.method == 'POST':
        uni = request.POST.get('university')
        dept = request.POST.get('department')
        session = request.POST.get('session')
        syllabus = request.FILES.get('syllabus')
        print(syllabus)
        syllabus_model = SyllabusModel(user=request.user, university=uni, department=dept, session=session,
                                       syllabus=syllabus, status=True)
        syllabus_model.save()
        return HttpResponseRedirect(reverse('App_content:syllabus'))
    return HttpResponseRedirect(reverse('App_content:syllabus'))


def syllabus_listview(request):
    syllabuses = SyllabusModel.objects.filter(status=True)
    syllabusForm = SyllabusModelForm()
    content = {
        'syllabuses': syllabuses,
        'syllabusForm': syllabusForm,
    }
    return render(request, 'App_content/syllabus_listview.html', context=content)


# -----------------------------------------------connections---------------------------------------- #

@login_required
def connection_request(request, user_id):
    from_user = request.user
    to_user = CustomUser.objects.get(id=user_id)
    connect_request, created = ConnectionRequestModel.objects.get_or_create(from_user=from_user, to_user=to_user)
    if created:
        return HttpResponse('Connection request sent')
    else:
        return HttpResponse('connection request was already sent')


@login_required
def accept_connection_request(request, request_id):
    connect_request = ConnectionRequestModel.objects.get(id=request_id)
    if connect_request.to_user == request.user:
        receiver_friend_list = ConnectionModel.objects.get_or_create(user=connect_request.to_user)
        receiver_friend_list[0].connections.add(connect_request.from_user)
        sender_friend_list = ConnectionModel.objects.get_or_create(user=connect_request.from_user)
        sender_friend_list[0].connections.add(connect_request.to_user)
        connect_request.is_active = True
        groupName = f"{connect_request.from_user.user_main_profile.fullName}"
        room = Room(name=groupName)
        room.save()
        findGrp = Group.objects.get_or_create(name=groupName)
        findGrp[0].user_set.add(connect_request.from_user)
        findGrp[0].user_set.add(connect_request.to_user)
        return HttpResponse('connection request is accepted.')
    else:
        return HttpResponse('request is not accepted.')


@login_required
def my_network_view(request):
    myNetworks = ConnectionModel.objects.filter(user=request.user)
    groups = request.user.groups.all()
    content = {
        'myNetworks': myNetworks[0],
    }
    return render(request, 'App_content/myNetworks.html', context=content)
