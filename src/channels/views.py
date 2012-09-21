# Create your views here.

import os
import re
import subprocess
import signal
import time
import logging
import socket

from channels.models import Channel
from hdhomerun.models import Device
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from django.core.urlresolvers import reverse

def index(request, hdid):
    t = loader.get_template('channels/index.htm')
    d = Device.objects.get(hdid=hdid)
    c = RequestContext(request, {
        'tuner_hdid': hdid,
        'channels': Channel.objects.filter(device=d).order_by('program'),
    })

    return HttpResponse(t.render(c))

def stop(request, hdid, vlc_pid):
    try:
        os.kill(int(vlc_pid), signal.SIGTERM)
    except OSError:
        pass

    return HttpResponseRedirect(reverse('channels-index', args=[ hdid ]))

def tune(request, hdid, channel, program):
    stream_ip = getIpAddress()
    port = '44322'
    tuner = '0'
    vlc_port = '8282'

    d = Device.objects.get(hdid=hdid)

    command = [
            "cvlc",
            "rtp://@:%s" % port,
            "--sout",
            "#transcode{vcodec=h264,width=512,vb=768,fps=25,venc=x264{vbv-bufsize=8192,vbv-maxrate=768,partitions=all,level=12,no-cabac,subme=7,threads=2,ref=2,mixed-refs=1,min-keyint=1,keyint=50,qpmax=51,bframes=0},acodec=mp4a,ab=48,channels=1,samplerate=44100,deinterlace,audio-sync}:standard{access=http{mime=video/mp4},mux=ts,dst=0.0.0.0:%s/stream.mp4}" % vlc_port
        ]

    with open(os.devnull, "w") as fnull:
        vlc_proc = subprocess.Popen(command, stdout=fnull, stderr=fnull)

        time.sleep(1) #Sleep for one second to let vlc get fully operational

        command = [ 'hdhomerun_config', hdid, 'set', '/tuner%s/channel' % tuner, 'auto:%s' % channel ]
        subprocess.call(command, stdout=fnull, stderr=fnull)

        command = [ 'hdhomerun_config', hdid, 'set', '/tuner%s/program' % tuner, program ]
        subprocess.call(command, stdout=fnull, stderr=fnull)

        command = [ 'hdhomerun_config', hdid, 'set', '/tuner%s/target' % tuner, 'rtp://%s:%s' % (stream_ip, port) ]
        subprocess.call(command, stdout=fnull, stderr=fnull)

    t = loader.get_template('channels/tune.htm')
    c = RequestContext(request, {
        'tuner_hdid': hdid,
        'vlc_pid': vlc_proc.pid,
        'video_url': 'http://%s:8282/stream.mp4' % stream_ip,
    })

    return HttpResponse(t.render(c))

def upload(request, hdid):
    if request.method == 'POST':
        channels_file = request.FILES['channels']

        resetChannelList(hdid, channels_file)

        return HttpResponseRedirect('index')

    t = loader.get_template('channels/upload.htm')
    c = RequestContext(request, {
        'tuner_hdid': hdid,
    })

    return HttpResponse(t.render(c))

def scan(request, hdid):
    command = [ 'hdhomerun_config', hdid, 'scan', '/tuner0' ]
    result = subprocess.check_output(command).split('\n')
    resetChannelList(hdid, result)
    return HttpResponseRedirect('index')

def resetChannelList(hdid, channelList):
    device = Device.objects.get(hdid=hdid)

    Channel.objects.filter(device=device).delete()

    current_channel = ''

    channel_pattern = re.compile('SCANNING.*us-cable:(\d+)')
    program_pattern = re.compile('PROGRAM\s(\d+):\s(?![0])(.*)')

    for line in channelList:
        m = channel_pattern.match(line)
        if m:
            current_channel = m.group(1)
        else:
            m = program_pattern.match(line)
            if m:
                c = Channel(device=device, channel=int(current_channel), program=int(m.group(1)), desc=m.group(2))
                c.save()

def getIpAddress():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("google.com",80))
    ip = s.getsockname()[0]
    s.close()

    return ip

