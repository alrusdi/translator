"""translator URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from translations.views import get_translations_info, suggest_translation
from ui import views

urlpatterns = [
    path('social-auth/', include('social_django.urls', namespace="social")),
    path('admin/', admin.site.urls),
    path("login/", views.login, name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("", views.home, name="home"),
    path("translations/", views.translations, name="translations"),
    path("get-translations-info/", get_translations_info, name="get_translations_info"),
    path("suggest-translation/", suggest_translation, name="suggest_translation"),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
