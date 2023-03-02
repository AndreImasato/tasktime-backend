FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    BUILD_DEPS="build-essential" \
    APP_DEPS="curl libcurl4-openssl-dev libssl-dev net-tools gcc netcat python3-dev musl-dev libpq-dev " \
    ENVIRONMENT="docker" \
    ROOT_DIR="/home/django/app"

RUN apt-get update \
    && apt-get install -y \
        ${BUILD_DEPS} \
        ${APP_DEPS} \
        --no-install-recommends

RUN addgroup --gid 3000 --system django \
    && adduser --uid 3000 --system --disabled-login --gid 3000 django \
    && mkdir -p ${ROOT_DIR} \
    && chown django:django -R ${ROOT_DIR}

WORKDIR ${ROOT_DIR}

COPY --chown=django:django ./requirements.txt ${ROOT_DIR}/requirements.txt

RUN pip install --upgrade --no-warn-script-location pip \
    && pip install --upgrade --no-warn-script-location setuptools \
    && pip install --no-warn-script-location --no-cache-dir -r requirements.txt

RUN rm -rf /var/lib/apt/lists/* \
    && rm -rf /usr/share/doc && rm -rf /usr/share/man \
    && apt-get purge -y --auto-remove ${BUILD_DEPS} \
    && apt-get clean

USER django
# Copy project
COPY --chown=django:django ./ ${ROOT_DIR}

RUN mkdir ${ROOT_DIR}/staticfiles \
    && mkdir ${ROOT_DIR}/mediafiles \
    && chown -R django:django ${ROOT_DIR}/ \
    && chown -R django:django ${ROOT_DIR}/staticfiles/ \
    && chown -R django:django ${ROOT_DIR}/mediafiles/ \
    && python manage.py collectstatic --no-input