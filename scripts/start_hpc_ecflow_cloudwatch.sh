#!/bin/bash

maindir=/home/vagrant/Documents/hpc-ecflow-cloudwatch/

uwsgi --http 10.31.99.60:8000 --wsgi-file ${maindir}app.py --callable app


