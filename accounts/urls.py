from accounts.views import AccountCreateView, LoginView, StatusCreateView

from django.conf.urls import url

urlpatterns = [
    url(r'^$', AccountCreateView.as_view(),
        name='create_account'),
    url(r'^login/$', LoginView.as_view(),
        name='login'),
    url(r'^status/$', StatusCreateView.as_view(),
        name='create_status'),
]
