#!/bin/bash

source /var/www/digitalem_project/venv/bin/activate

gunicorn --workers 3 \
  --bind unix:/var/www/digitalem_project/digitalem_project.sock \
  digitalem_project.wsgi:application
