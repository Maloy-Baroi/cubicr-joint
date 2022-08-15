from django.urls import path
from App_content import views

app_name = 'App_content'

urlpatterns = [
    path('new-podcast/', views.new_podcast, name='new-podcast'),
    path('pod-showcase/', views.podcast_listview, name='pod-showcase'),
    path('new-post/', views.new_post, name='new-post'),
    path('post-listview/', views.post_listview, name='post-listview'),
    path('love-react/<int:pk>/', views.post_love, name='love-react'),
    path('no-love-react/<int:pk>/', views.post_no_loved, name='no-love-react'),
    path('syllabus/', views.syllabus_listview, name='syllabus'),
    path('add-syllabus/', views.add_syllabus, name='add-syllabus'),
    path('make-status-false/<int:pk>/', views.make_post_status_false, name='make-status-false'),
    path('make-podcast-status-false/<int:pk>/', views.make_pod_status_false, name='make-podcast-status-false'),
    path('connection-request/<int:user_id>/', views.connection_request, name='connection-request'),
    path('accept-connection-request/<int:request_id>/', views.accept_connection_request,
         name='accept-connection-request'),
    path('my-network-view/', views.my_network_view, name='my-network-view'),
]
