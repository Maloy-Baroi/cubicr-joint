from django.urls import path
from App_auth.views import *

app_name = 'App_auth'

urlpatterns = [
    # path('home/', home, name='home'),
    path('register/', signup_view, name='register'),
    path('register-attempt/', signup_attempt, name='register-attempt'),
    path('login/', login_view, name='login'),
    path('token-send/', token_send, name='token-send'),
    path('verify/<auth_token>/', verify, name="verify"),
    path('error', error_page, name="error"),
    path('logout/', logout_view, name='logout'),
    path('profile-setup/', profile_setup, name='profile-setup'),
    path('profile-view/', profile_view, name='profile-view'),
    path('add-new-education/', add_new_education, name='add-new-education'),
    path('add-new-experience/', add_new_experience, name='add-new-experience'),
    path('add-new-skill/', add_new_skill, name='add-new-skill'),
    path('add-new-extra-curriculum/', add_new_extra_curriculum, name='add-new-extra-curriculum'),
    path('add-new-co-curriculum/', add_new_co_curriculum, name='add-new-co-curriculum'),
    path('general-profile-settings/', general_profile_settings, name='general-profile-settings'),
    path('update-password/', password_update, name='update-password'),
    path('cv-open/', cv_generate, name='cv-open'),
    path('add-reference/', add_reference, name='add-reference'),
    path('create-cv-pdf/', pdf_generator, name='create-cv-pdf'),
    path('cv-generator-2/', cv_generator_2, name='cv-generator-2'),
]
