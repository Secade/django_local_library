"""locallibrary URL Configuration

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
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
]

from django.urls import include
from django.urls import path

urlpatterns += [
    path('catalog/', include('catalog.urls'), name="catalog"),
]

from django.views.generic import RedirectView

urlpatterns += [
    path('',RedirectView.as_view(url='catalog/',permanent=True)),
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
]

handler404 = 'catalog.views.error_404'
handler403 = 'catalog.views.error_403'

urlpatterns += [
    path('session_security/', include('session_security.urls')),
]

from catalog.views import signup_view, lockout_view
from catalog.views import passwordReset_view
from catalog.views import emailRequest_view
from catalog.views import changePassword_view
urlpatterns += [
    path('signup/', signup_view, name="signup"),
    path('accounts/login/lockout/', lockout_view, name="lockout"),
    path('emailreset/', emailRequest_view, name="email-request"),
    path('passwordreset/', passwordReset_view, name='reset'),
    path('passwordchange/', changePassword_view, name='change-password'),
]
