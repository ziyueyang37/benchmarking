#!/bin/bash

for FILE in ./esm_fixed/*
do
    ./p2rank/prank.sh predict -f $FILE
done
