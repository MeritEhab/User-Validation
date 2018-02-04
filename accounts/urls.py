from django.conf.urls import url
from accounts.views import AccountCreateView

urlpatterns = [
    url(r'^$', AccountCreateView.as_view(),
        name='create_account'),
]
