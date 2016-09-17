from django.conf.urls import url

from apps.logger.api.views import ReadingElectricityUsedView, \
    ReadingElectricityDeliveredView, ReadingGasUsedView, \
    ElectricityActualUsageView, ElectricityActualDeliveryView

url_patterns = {
    url(r'^readings/electricity/usage/total/(?P<aggregate>\w+)/$',
        ReadingElectricityUsedView.as_view()),
    url(r'^readings/electricity/delivery/total/(?P<aggregate>\w+)/$',
        ReadingElectricityDeliveredView.as_view()),
    url(r'^readings/electricity/usage/actual/(?P<aggregate>\w+)/$',
        ElectricityActualUsageView.as_view()),
    url(r'^readings/electricity/delivery/actual/(?P<aggregate>\w+)/$',
        ElectricityActualDeliveryView.as_view()),
    url(r'^readings/gas/usage/total/(?P<aggregate>\w+)/$',
        ReadingGasUsedView.as_view()),
}
