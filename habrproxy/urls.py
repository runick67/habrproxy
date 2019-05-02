from django.conf.urls import url

from habr_proxy import habr_proxy

urlpatterns = [
    url(r'^(?P<path>.*)$', habr_proxy),
]
