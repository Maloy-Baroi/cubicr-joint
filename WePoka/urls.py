"""WePoka URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

from App_auth.views import home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('App_auth.urls')),
    path('', home, name='home'),
    path('post/', include('App_post.urls')),
    path('content/', include('App_content.urls')),
    path('chat/', include('App_chat.urls')),
    #     Reset Password
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='App_auth/password_reset.html'),
         name='password_reset'),
    path('reset-password-confirm/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='App_auth/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('reset-password-done/',
         auth_views.PasswordResetDoneView.as_view(template_name='App_auth/password_reset_done.html'),
         name='password_reset_done'),
    path('reset-password-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='App_auth/password_reset_complete.html'),
         name='password_reset_complete'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
