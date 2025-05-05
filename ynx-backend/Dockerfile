FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1
WORKDIR /ynx-backend
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
COPY . /ynx-backend
RUN chmod a+x *.sh
EXPOSE 8000