from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from django.views.generic.base import RedirectView

urlpatterns = patterns('',
    # Examples:



     url(r'^$', 'barylka_django.web.views.index', name='index'),
     url(r'^edycja/2/$', RedirectView.as_view(url='/', permanent=False)),
     url(r'^edycja/(\d)/$', 'barylka_django.web.views.index', name='index'),

     url(r'^ranking/$', 'barylka_django.web.views.rank', name='rank'),
     url(r'^ranking/2/$', RedirectView.as_view(url='/ranking/', permanent=False)),
     url(r'^ranking/(\d)/$', 'barylka_django.web.views.rank', name='rank'),


     url(r'^ludzie/([\w-]*)/$', 'barylka_django.web.views.user', name='user'),

     url(r'^crawl$', 'barylka_django.crawler.micro_crawler.crawl', name='crawl'),

    # url(r'^barylka_django/', include('barylka_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
