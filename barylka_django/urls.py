from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
     url(r'^$', 'barylka_django.web.views.index', name='index'),
     url(r'^ludzie/([\w-]*)/$', 'barylka_django.web.views.user', name='user'),
     url(r'^ranking/$', 'barylka_django.web.views.rank', name='rank'),

     url(r'^scrap$', 'barylka_django.scrapper.scrap_micro.scrap', name='scrap'),
     url(r'^import_data$', 'barylka_django.scrapper.scrap_micro.import_data', name='import_data'),

    # url(r'^barylka_django/', include('barylka_django.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
