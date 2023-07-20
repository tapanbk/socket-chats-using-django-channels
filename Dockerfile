FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app
RUN pip install --upgrade pip \
    && pip install --no-cache-dir --requirement requirements.txt
CMD "/bin/bash"