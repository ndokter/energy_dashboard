from django.conf.urls import url

from apps.dashboard.views import Index


urlpatterns = [
    url(r'^$', Index.as_view(), name='index'),
]