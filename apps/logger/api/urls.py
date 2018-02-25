from django.conf.urls import url

from apps.logger.api.views import ElectricityUsedView, \
    ElectricityDeliveredView, GasUsedView, \
   ElectricityActualUsageView, ElectricityActualDeliveryView

url_patterns = {
    url(r'^metrics/electricity/usage/total/(?P<aggregate>\w+)/$',
        ElectricityUsedView.as_view()),
    url(r'^metrics/electricity/delivery/total/(?P<aggregate>\w+)/$',
        ElectricityDeliveredView.as_view()),
    url(r'^metrics/electricity/usage/actual/(?P<aggregate>\w+)/$',
        ElectricityActualUsageView.as_view()),
    url(r'^metrics/electricity/delivery/actual/(?P<aggregate>\w+)/$',
        ElectricityActualDeliveryView.as_view()),
    url(r'^metrics/gas/usage/total/(?P<aggregate>\w+)/$',
        GasUsedView.as_view()),
}
