"""django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import include
from django.conf import settings

urlpatterns = [
    path("", include("main.urls")),
    #  path("main/", include("main.urls")),
    path('admin/', admin.site.urls),
]

# Add source assets locations...
if settings.LOCAL:
    from django.conf.urls.static import static
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.ASSETS_URL, document_root=settings.ASSETS_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

#  # TODO: Add different location depnding on dev/prod mode (see examples below)...
#  if settings.DEBUG:
#      pass
#      urlpatterns += patterns(
#          '',
#          # url(r'^400/$', TemplateView.as_view(template_name='400.html.django')),
#          url(r'^403/$', TemplateView.as_view(template_name='403.html.django')),
#          url(r'^404/$', 'django.views.defaults.page_not_found'),
#          url(r'^500/$', 'django.views.defaults.server_error'),
#      )
#  else:
#      #  handler403 = views.page403
#      #  handler404 = views.page404
#      #  handler500 = views.page500

handler403 = 'main.views.page403'
handler404 = 'main.views.page404'
handler500 = 'main.views.page500'
