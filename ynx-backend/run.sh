#!/bin/bash

cd  src
if [[ "${1}" == "celery" ]]; then
    celery --app=utils.worker.celery worker --loglevel=info
elif [[ "${1}" == "flower" ]]; then
    celery --app=utils.worker.celery flower
elif [[ "${1}" == "main" ]]; then
    uvicorn main:app --reload
fi