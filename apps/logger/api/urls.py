from django.conf.urls import url

from apps.logger.api.views import ReadingReportView

url_patterns = [
    url(r'^meter/(?P<meter_id>\d+)/readings/(?P<aggregate>\w+)/$', ReadingReportView.as_view()),
]
