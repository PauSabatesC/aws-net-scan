#!/usr/bin/env bash

#set -x

ENV=$1
#unset $(grep -v '^#' ./$ENV.env | sed 's/\=.*/''/g')

if [ -d 'dist' ] ; then
    rm -r dist
fi

if [ -d 'site' ] ; then
    rm -r site
fi

if [ -d 'venv' ] ; then
    rm -rf venv
fi

rm -rf *.pyc

deactivate
