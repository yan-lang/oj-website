"""website URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.contrib.auth import logout
from django.urls import path, include
from django_registration.backends.activation.views import RegistrationView
from account.forms import CustomRegistrationForm
from django.contrib.auth.views import LoginView

urlpatterns = [
    path('admin/', admin.site.urls),
]

# Add Django site authetication and registeration urls
# https://django-registration.readthedocs.io/en/3.1/quickstart.html#required-templates
urlpatterns += [
    path('accounts/register/',
         RegistrationView.as_view(form_class=CustomRegistrationForm),
         name='django_registration_register',
         ),
    path('accounts/', include('django_registration.backends.activation.urls')),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

# Setting
urlpatterns += [
    path('settings/', include('settings.urls'))
]

# Add our application urls

urlpatterns += [
    path('oj/', include('oj.urls'))
]

# Add URL maps to redirect the base URL to our application

from django.views.generic import RedirectView

urlpatterns += [
    path('', RedirectView.as_view(url='/oj/index', permanent=True)),
]

urlpatterns += [
    path('mdeditor/', include('mdeditor.urls'))
]

# static files (images, css, javascript, etc.)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

"""
Restful API
"""

from rest_framework.schemas import get_schema_view
from rest_framework.documentation import include_docs_urls

API_TITLE = 'OJ API'
API_DESCRIPTION = 'A Web API for evaluating programming assignments.'
schema_view = get_schema_view(title=API_TITLE)

urlpatterns += [
    path('api/auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('api/schema/', schema_view),
    path('api/docs/', include_docs_urls(title=API_TITLE, description=API_DESCRIPTION))
]

urlpatterns += [
    path('api/', include('account.rest_urls'))
]
