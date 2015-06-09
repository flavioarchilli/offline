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

Deploying to a virtual machine
------------------------------

Running locally is all well and good, but ideally you will want a uniform development environment across your team, and parity between your development and production environments.

A nice way of doing this is to run the application on a virtual machine (VM) which mirrors the production environment.
This example application can be run on a [Scientific Linux](https://www.scientificlinux.org/) 6.4 VM which is managed by [Vagrant](https://www.vagrantup.com/).
Once you have [installed Vagrant](https://docs.vagrantup.com/v2/installation/index.html), the VM can be set up by running the following commands inside this repository.

```bash
# Run the initial provision
$ vagrant up --provision
# Run the second provisioning once prompted to do so
$ vagrant reload --provision
# One final reboot
$ vagrant reload
```

You can then SSH in to the machine and run the set up script, which installs the example application's dependencies.

```bash
# On the host machine
$ vagrant ssh
# Now on the VM
$ cd /vagrant
$ ./setup_monitoring_app.sh
```

To run the application, activate the `virtualenv` and start the web server, worker instances, and Redis database using the [Honcho](https://pypi.python.org/pypi/honcho) process manager.

```bash
$ cd /vagrant
$ workon monitoring_app
$ honcho start -c worker=4
```

You can the [view the example application](http://localhost:5000/) on the host.

![Two histograms being shown on the grid layout page in the example application.](https://dl.dropboxusercontent.com/u/37461/example-monitoring-app.png)
