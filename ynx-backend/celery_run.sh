#!/bin/bash

cd src
celery --app=utils.worker.celery worker --loglevel=info