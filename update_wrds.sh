#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
cd $DIR

printf "Intializing\n"
## Use conda for managing python environment
source ~/anaconda3/etc/profile.d/conda.sh
conda activate wrds
## Pull in latest update
git pull
source env.sh
python ./main.py "$@"
