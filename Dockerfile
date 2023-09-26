#FROM python:3.9-slim-buster
#
#ENV PYTHONUNBUFFERED=1 \
#    PYTHONDONTWRITEBYTECODE=1 \
#    PIP_NO_CACHE_DIR=off \
#    PIP_DISABLE_PIP_VERSION_CHECK=on \
#    PIP_DEFAULT_TIMEOUT=100 \
#    PYSETUP_PATH="/opt/pysetup" \
#    VENV_PATH="/opt/pysetup/.venv"
#
#ENV PATH="$VENV_PATH/bin:$PATH"
#
## Install Dependencies
#
#RUN set -ex \
#    && apt-get update \
#    && apt-get install -y --no-install-recommends \
#    build-essential zlib1g-dev libncurses5-dev libgdbm-dev libnss3-dev libssl-dev libreadline-dev libffi-dev  \
#    libsqlite3-dev wget libbz2-dev gcc  \
#    && rm -rf /var/lib/apt/lists/*
#
#RUN pip install --upgrade pip
#
## Builder base
#
## Install dependencies
#RUN python -m venv $VENV_PATH
#
#WORKDIR $PYSETUP_PATH
#
#COPY requirements.txt ./
#
#RUN pip install --upgrade pip \
#    && pip install --no-cache-dir --requirement requirements.txt
#COPY ./ $PYSETUP_PATH
#ENTRYPOINT ["application_runner.sh"]
#
#EXPOSE 8000
#
#ENTRYPOINT sh -c "python manage.py runserver 0.0.0.0:8000"


FROM python:3.10-alpine

ENV PYTHONUNBUFFERED=1

RUN apk update \
    && apk add --no-cache --virtual .build-deps \
    ca-certificates gcc linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev libc-dev \
    postgresql-dev cargo

RUN pip install --upgrade pip

# Create group and user
RUN addgroup chat && adduser -D chat -G chat -h /home/chat

ENV HOME /home/chat

ENV APP_DIR ${HOME}/socket_chat

WORKDIR ${APP_DIR}

ADD requirements.txt ${APP_DIR}/

RUN pip install -r ${APP_DIR}/requirements.txt


#COPY ./application_runner.sh ${WORKDIR}/application_runner.sh
#RUN chmod +x ${WORKDIR}/application_runner.sh

COPY ./ ${APP_DIR}

RUN chown -R chat:chat ${APP_DIR}

USER chat

EXPOSE 8000

#ENTRYPOINT sh -c "python manage.py runserver 0.0.0.0:8000"

ENTRYPOINT ["./application_runner.sh"]

#ENTRYPOINT ["/home/chat/socket_chat/application_runner.sh"]

#COPY . .
#
## new
## run entrypoint.sh
#ENTRYPOINT ["/usr/src/app/entrypoint.sh"]

#ENTRYPOINT ["application_runner.sh"]
##
#ENTRYPOINT sh -c "python manage.py runserver 0.0.0.0:8000"

#ENTRYPOINT ["sh", "-c", "$APP_DIR/application_runner.sh"]

