from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'hdhomerun_streamer.views.home', name='home'),
    # url(r'^hdhomerun_streamer/', include('hdhomerun_streamer.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),

    url(r'^$', 'hdhomerun.views.index'),

    url(r'^(?P<hdid>[A-F0-9]+)/channels/index$', 'channels.views.index', name='channels-index'),
    url(r'^(?P<hdid>[A-F0-9]+)/channels/upload$', 'channels.views.upload', name='channels-upload'),
    url(r'^(?P<hdid>[A-F0-9]+)/channels/scan$', 'channels.views.scan'),
    url(r'^(?P<hdid>[A-F0-9]+)/channels/tune/(?P<channel>\d+)/(?P<program>\d+)$', 'channels.views.tune', name='channels-tune'),
    url(r'^(?P<hdid>[A-F0-9]+)/channels/stop/(?P<vlc_pid>\d+)$', 'channels.views.stop', name='channels-stop'),

    url(r'^hdhomerun/setup$', 'hdhomerun.views.setup', name='hdhomerun-setup'),
    url(r'^hdhomerun/index$', 'hdhomerun.views.index', name='hdhomerun-index'),
)
