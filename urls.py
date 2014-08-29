from django.conf.urls import patterns, include, url
from django.conf import settings
#import haystack
from django.contrib import admin
from django.http import HttpResponse

#haystack.autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
#    (r'^search/', include('haystack.urls')),
)

urlpatterns += patterns('',
    url(r'^', include('cms.urls')),
    url(r'^robots.txt', lambda request: HttpResponse("User-agent: *\nAllow: /\n")),
    # (r'^tinymce/', include('tinymce.urls')),
)


if settings.DEBUG:
    urlpatterns = patterns('',
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    url(r'', include('django.contrib.staticfiles.urls')),
) + urlpatterns
