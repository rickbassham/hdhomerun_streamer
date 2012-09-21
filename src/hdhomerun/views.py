# Create your views here.

import logging

import re
import subprocess
import signal

from hdhomerun.models import Device

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader

def index(request):
    t = loader.get_template('hdhomerun/index.htm')
    c = RequestContext(request, {
        'devices': Device.objects.all(),
    })

    return HttpResponse(t.render(c))


def setup(request):

    Device.objects.all().delete()

    command = [ 'hdhomerun_config', 'discover' ]
    result = subprocess.check_output(command).split('\n')

    discover_pattern = re.compile('hdhomerun device ([A-F0-9]+) found at .*')

    for line in result:
        logging.debug(line)

        m = discover_pattern.match(line)
        if m:
            hdid = m.group(1)

            logging.debug(hdid)

            try:
                existing = Device.objects.get(hdid=hdid)
            except Device.DoesNotExist:
                d = Device(hdid=hdid)
                d.save()

    all_devices = Device.objects.all()

    if (all_devices.count() == 1):
        return HttpResponseRedirect('../%s/channels/index' % all_devices[0].hdid)

    return HttpResponseRedirect('../hdhomerun/index')

