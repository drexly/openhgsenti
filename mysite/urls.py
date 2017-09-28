"""deff URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/dev/topics/http/urls/
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

from django.contrib.auth import views as autho
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from quots.views import *
import mysite.settings


urlpatterns = [
    url(r'^$', index),
    url(r'^search/', search),
    url(r'^admin/', admin.site.urls),
    url(r'^login/',autho.login,{'template_name':'login.html'},name='login'),
    url(r'^logout/',autho.logout,{'template_name':'index.html'},name='logout'),
    url(r'^register/$',register,name='register'),
    url(r'^apicall/', apicall),
    url(r'^jsonapi/(?P<userid>.*)/(?P<keyword>.*)/$',jsonapi,name='jsonapi'),
]
urlpatterns += static(mysite.settings.MEDIA_URL, document_root=mysite.settings.MEDIA_ROOT)


