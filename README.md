# Monitoring app [![Build status](https://travis-ci.org/alexpearce/example-monitoring-app.svg)](http://travis-ci.org/alexpearce/example-monitoring-app)

An example monitoring application deriving from the [`jobmonitor`](https://github.com/alexpearce/jobmonitor).

Change here.

Setup
-----

Clone the repository, set up a [`virtualenv`](http://virtualenv.readthedocs.org/en/latest/) (with [`virtualenvwrapper`](http://virtualenvwrapper.readthedocs.org/en/latest/)), generate some data, then run the application.

```bash
$ git clone https://github.com/alexpearce/example-monitoring-app.git
$ cd example-monitoring-app
$ mkvirtualenv monitoring-app
$ pip install -r requirements.txt
$ cd monitoring_app/static/files
$ python generate_histograms.py
$ cd ../../..
$ honcho start
```

The `honcho start` command will initialise the application, a [Redis](http://redis.io/) server, and one worker.
To start more than one worker, you can use the `-c` option like `honcho start -c worker=4`.

Requirements
------------

A [Redis](http://redis.io/) server is used to queuing jobs and storing their results.
[ROOT](http://root.cern.ch/) is used to perform the tasks, namely getting data out of histograms, and to generate the data in the first place.


