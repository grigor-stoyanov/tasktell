from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from tasktell.main.views import home_view

urlpatterns = [
    path('', home_view, name='home')
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
