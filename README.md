hdhomerun_streamer
==================

A django web app for initiating a stream from an hdhomerun tuner. Able to stream to android.

git clone https://github.com/rickbassham/hdhomerun_streamer.git

cd hdhomerun_streamer/src

./manage.py syncdb

./manage.py runserver 0.0.0.0:8000

Browse to http://localhost:8000/

Scan for new devices...

Upload channels file...

Click on a channel to start transcoding...

Click watch to start watching...

Be sure to click stop when you are done, or you will continue transcoding and waste cpu cycles.
