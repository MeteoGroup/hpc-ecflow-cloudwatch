#!/bin/bash

source /etc/profile.d/modules.sh
module load ecflow/gcc/current

exec "$@"
