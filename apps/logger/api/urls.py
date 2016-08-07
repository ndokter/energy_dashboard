from django.conf.urls import url

from apps.logger.api.views import ReadingElectricityUsedView, \
    ReadingElectricityDeliveredView, ReadingGasUsedView

url_patterns = [
    url(r'^readings/electricity/used/(?P<aggregate>\w+)/$',
        ReadingElectricityUsedView.as_view()),
    url(r'^readings/electricity/delivered/(?P<aggregate>\w+)/$',
        ReadingElectricityDeliveredView.as_view()),
    url(r'^readings/gas/used/(?P<aggregate>\w+)/$',
        ReadingGasUsedView.as_view()),
]
