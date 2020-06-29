"""canvas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth.views import LoginView

from accounts.forms import LoginForm


urlpatterns = [
    url(r'^$', LoginView.as_view(
            form_class=LoginForm,
            template_name='registration/login.html',
            redirect_authenticated_user=True
        ), name='home'),
    url(r'^lightshow/', admin.site.urls),
    url(r'^account/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^reviews/', include('reviews.urls', namespace='reviews')),
    url(r'^search/', include('haystack.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
