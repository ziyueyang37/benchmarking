#!/bin/bash
bash devtools/install.sh

export PATH=`pwd`/anaconda/bin:$PATH
source activate ml_starter

python my_experiment.py
pytest test_all.py --junitxml=test_results.xml
