#!/bin/bash

VIRTUAL_ENV="venv"
ENV=$1
if [[  ! -d "$VIRTUAL_ENV" ]]
then
    echo "$DIRECTORY does exists on your filesystem. Creating it..."
    sudo apt install python3.7-venv
    python3.7 -m venv venv
fi

echo "$DIRECTORY found in your directory. Activating it and setting $ENV environment variables..."

source venv/bin/activate

#export $(grep -v '^#' ./$ENV.env | xargs)

pip install -e .
echo "Finished."

