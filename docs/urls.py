from django.conf.urls import patterns, include, url
from django.contrib import admin
from simple_sso.sso_client.client import Client
from django.conf import settings

sso_client = Client(server_url=settings.SSO_SERVER_URL,
	                public_key=settings.SSO_PUBLIC_KEY,
	                private_key=settings.SSO_PRIVATE_KEY)

urlpatterns = patterns('',
    url(r'^sso/', include(sso_client.get_urls())),
    url(r'^$', 'docs.views.home', name='home'),
    url(r'^login$', 'docs.views.login', name='login'),
    # Examples:
    # url(r'^$', 'docs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^admin/', include(admin.site.urls)),
)