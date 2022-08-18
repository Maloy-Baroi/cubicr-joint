from django.urls import path
from . import views

app_name = 'App_post'

urlpatterns = [
    # path('', views.home, name='home'),
    path('partner-request/', views.partner_request_view, name='partner-request'),
    path('partner-request-post/', views.partner_request_form_post, name='partner-request-post'),
    path('my-project-n-partner-view/', views.my_project_n_partner_view, name='my-project-n-partner-view'),
    path('job-post/', views.job_post, name='job-post'),
    path('apply/<int:pk>/', views.apply_for_participation, name='apply-for-participation'),
    path('partner-request/<int:pk>/', views.apply_for_participation, name='partner-request-description'),
    path('display-job-posts/', views.display_job_list, name='display-job-post'),
    path('single-job-post/<int:pk>/', views.single_job_view, name='single-job-post'),
    path('apply-for-job/<int:pk>/', views.apply_for_job, name='apply-for-job'),
    path('accept-apply-for-research-participation/<int:user_id>/<int:pnr_apply_id>/',
         views.accept_apply_for_research_participation,
         name='accept-apply-for-research-participation'),
    path('research-papers/', views.research_papers_view, name='research-papers'),
]
