#!/bin/bash

maindir=/home/vagrant/Documents/hpc-ecflow-cloudwatch/

module load ecflow/intel/4.7.1

#export PYTHONPATH=/usr/lib/python2.7/site-packages
export PYTHONPATH=${PYTHONPATH}:${maindir}/dao
export PYTHONPATH=${PYTHONPATH}:${maindir}/main
export PYTHONPATH=${PYTHONPATH}:${maindir}/utils
export PYTHONPATH=${PYTHONPATH}:${maindir}/
rm -f uwsgi.log

echo $PYTHONPATH

#uwsgi --http 10.31.41.24:8000 --wsgi-file ${maindir}app.py --callable app --logto uwsgi.log
python ${maindir}app.py

