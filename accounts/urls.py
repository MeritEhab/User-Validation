from django.conf.urls import url
from accounts.views import AccountCreateView, LoginView

urlpatterns = [
    url(r'^$', AccountCreateView.as_view(),
        name='create_account'),
    url(r'^login/$', LoginView.as_view(),
        name='login'),
]
