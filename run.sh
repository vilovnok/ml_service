#!/bin/bash


if [[ "${1}" == "celery" ]]; then
    cd ynx-backend/src/
    celery --app=utils.worker.celery worker --loglevel=info
elif [[ "${1}" == "flower" ]]; then
    celery --app=utils.worker.celery flower
elif [[ "${1}" == "ba" ]]; then
    cd ynx-backend/src/
    uvicorn main:app --reload
elif [[ "${1}" == "fr" ]]; then
    cd ynx-frontend
    ng serve --port 4200
fi